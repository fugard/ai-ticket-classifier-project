import json
import logging
import re
from typing import Dict, List

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from config import AWS_REGION, BEDROCK_MODEL_ID
from models import ClassificationResult

logger = logging.getLogger(__name__)

CATEGORY_RULES = [
    {
        "category": "Billing",
        "team": "Finance",
        "priority": "High",
        "keywords": ["charged", "refund", "invoice", "billing", "payment", "subscription", "double charge"],
        "response": "Thanks for contacting support. We are sorry about the billing issue. Your case has been prioritised and sent to our finance team for review."
    },
    {
        "category": "Technical Support",
        "team": "Engineering",
        "priority": "High",
        "keywords": ["error", "bug", "crash", "not working", "issue", "failed", "failure", "upload"],
        "response": "Thanks for reporting the technical issue. We have prioritised your case and routed it to our engineering team for investigation."
    },
    {
        "category": "Account Access",
        "team": "Security",
        "priority": "High",
        "keywords": ["login", "log in", "password", "reset link", "locked", "access", "sign in"],
        "response": "Thanks for contacting support. We can see this is an account access issue and have routed it to the security support team for urgent assistance."
    },
    {
        "category": "Feature Request",
        "team": "Product",
        "priority": "Low",
        "keywords": ["feature", "would be great", "please add", "enhancement", "improve", "dark mode"],
        "response": "Thanks for the suggestion. We have recorded your feature request and shared it with the product team for consideration."
    },
    {
        "category": "Complaint",
        "team": "Customer Success",
        "priority": "Medium",
        "keywords": ["unhappy", "complaint", "poor service", "delay", "escalate", "disappointed"],
        "response": "We are sorry to hear about your experience. Your concern has been escalated to our customer success team for review."
    },
]

DEFAULT_RESULT = ClassificationResult(
    category="General Inquiry",
    priority="Low",
    team="Support",
    confidence=0.60,
    suggested_response="Thanks for contacting support. Your request has been received and assigned to our support team.",
    model_source="heuristic",
)


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def classify_with_heuristics(message: str) -> ClassificationResult:
    text = _normalise(message)
    best_match = None
    best_score = 0

    for rule in CATEGORY_RULES:
        score = sum(1 for keyword in rule["keywords"] if keyword in text)
        if score > best_score:
            best_score = score
            best_match = rule

    if not best_match:
        return DEFAULT_RESULT

    confidence = min(0.70 + (0.08 * best_score), 0.98)
    return ClassificationResult(
        category=best_match["category"],
        priority=best_match["priority"],
        team=best_match["team"],
        confidence=round(confidence, 2),
        suggested_response=best_match["response"],
        model_source="heuristic",
    )


def _build_prompt(message: str) -> str:
    return f"""
You are an AI support operations assistant.

Analyse the customer support ticket below and return ONLY valid JSON.

Required JSON keys:
- category
- priority
- team
- confidence
- suggested_response
- model_source

Allowed categories:
Billing, Technical Support, Account Access, Feature Request, Complaint, General Inquiry

Allowed priorities:
Low, Medium, High

Ticket:
{message}
""".strip()


def classify_with_bedrock(message: str) -> ClassificationResult:
    if not BEDROCK_MODEL_ID:
        raise ValueError("BEDROCK_MODEL_ID is not configured")

    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    prompt = _build_prompt(message)
    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 300,
            "temperature": 0.2,
            "topP": 0.9
        }
    }

    response = client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    payload = json.loads(response["body"].read().decode("utf-8"))

    generated_text = ""
    if isinstance(payload, dict):
        if "results" in payload and payload["results"]:
            generated_text = payload["results"][0].get("outputText", "")
        elif "outputText" in payload:
            generated_text = payload["outputText"]

    parsed = json.loads(generated_text)
    return ClassificationResult(
        category=parsed["category"],
        priority=parsed["priority"],
        team=parsed["team"],
        confidence=float(parsed["confidence"]),
        suggested_response=parsed["suggested_response"],
        model_source=parsed.get("model_source", "bedrock"),
    )


def classify_ticket(message: str) -> ClassificationResult:
    if not message or not message.strip():
        raise ValueError("Ticket message is required")

    if BEDROCK_MODEL_ID:
        try:
            result = classify_with_bedrock(message)
            result.model_source = "bedrock"
            return result
        except (BotoCoreError, ClientError, ValueError, KeyError, json.JSONDecodeError) as exc:
            logger.warning("Bedrock classification failed; falling back to heuristics: %s", exc)

    return classify_with_heuristics(message)

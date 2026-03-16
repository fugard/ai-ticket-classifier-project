import json
import logging
from typing import Any, Dict

from ai_classifier import classify_ticket
from config import LOG_LEVEL
from storage import publish_notification, save_ticket

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


def _response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        message = body.get("message", "")

        classification = classify_ticket(message).to_dict()
        ticket = save_ticket(message, classification)
        publish_notification(ticket)

        return _response(
            200,
            {
                "ticket_id": ticket["ticket_id"],
                "category": ticket["category"],
                "priority": ticket["priority"],
                "team": ticket["team"],
                "confidence": ticket["confidence"],
                "suggested_response": ticket["suggested_response"],
                "model_source": ticket["model_source"],
            },
        )
    except ValueError as exc:
        logger.warning("Validation error: %s", exc)
        return _response(400, {"error": str(exc)})
    except Exception as exc:
        logger.exception("Unhandled application error")
        return _response(500, {"error": "Internal server error", "detail": str(exc)})

import json
import logging
from datetime import datetime, timezone
from typing import Dict
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

from config import AWS_REGION, NOTIFICATIONS_TOPIC_ARN, TICKETS_TABLE

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
sns = boto3.client("sns", region_name=AWS_REGION)


def save_ticket(message: str, classification: Dict) -> Dict:
    table = dynamodb.Table(TICKETS_TABLE)

    item = {
        "ticket_id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "original_message": message,
        **classification,
    }

    table.put_item(Item=item)
    return item


def publish_notification(ticket: Dict) -> None:
    if not NOTIFICATIONS_TOPIC_ARN:
        logger.info("SNS topic ARN not configured; skipping notification")
        return

    try:
        sns.publish(
            TopicArn=NOTIFICATIONS_TOPIC_ARN,
            Subject=f"New support ticket: {ticket['category']}",
            Message=json.dumps(ticket, indent=2),
        )
    except ClientError as exc:
        logger.error("Failed to publish SNS notification: %s", exc)
        raise

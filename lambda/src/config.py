import os

TICKETS_TABLE = os.getenv("TICKETS_TABLE", "tickets-local")
NOTIFICATIONS_TOPIC_ARN = os.getenv("NOTIFICATIONS_TOPIC_ARN", "")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

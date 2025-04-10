
import json
import logging
import os
from typing import Any, Dict

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger()
logger.setLevel(log_level)


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a Lambda response object.

    Args:
        status_code: HTTP status code
        body: Response body

    Returns:
        Lambda response dictionary
    """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return create_response(400, {"error": "Invalid JSON"})

    return create_response(200, body)


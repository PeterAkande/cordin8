import json
import logging
import traceback
from decorators.authentication_n_authorizer_decorator import cordin8_api
from proxy_response_handler.api_exception import APIServerError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cordin8_api(authorized=True)
def lambda_handler(event, context, user_details=None, access_token=None):
    """
    This function would handle accepting an invitation and Rejecting an invitation
    """

    logger.info(f"This is the user details {user_details}")
    logger.info(f"This is the Event  {event}")

    profile_type = user_details.get("profile_type", None)

    if profile_type != "user":
        APIServerError(
            "Only users can accept and reject an invitation", status_code=400
        )

    user_id = user_details.get("profile_id", None)

    if user_id is None:
        APIServerError(
            "Only users can accept and reject an invitation", status_code=400
        )

    try:
        body = json.loads(event["body"])
        http_method = event["httpMethod"]
    except Exception as e:
        traceback.print_exc()

        raise APIServerError("Bad Request, Cant parse body", status_code=400)


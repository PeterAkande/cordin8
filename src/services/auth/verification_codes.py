import json
import traceback

from proxy_response_handler.api_exception import APIServerError
from proxy_response_handler.simple_response import SimpleResponse
from utils.cognito_utils import Cordin8CognitoHandler
from utils.dynamo_db_handlers.user_db_handler import UserDynamoDbHandler


def lambda_handler(event, context, access_token=None):
    """
    This would handle sending a verification code to the user.
    A POST request would mean that the user is to be verified.
    """

    try:
        body = json.loads(event.get("body", {}))
    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)

    cognito_handler = Cordin8CognitoHandler()

    # Get the email and the code from the body
    email = body.get("email", None)

    if email is None:
        return APIServerError("Please give the email of the user", status_code=400)

    # Get the id of the user
    (
        operation_success,
        error_message,
        email_verified,
        user_id,
    ) = cognito_handler.get_user_details_from_cognito(email=email)

    if not operation_success:
        return APIServerError(operation_success, status_code=400)

    if email_verified:
        return APIServerError("User is verified aleady", status_code=400)

    success, message = cognito_handler.resend_verification_code(email=email)

    if not success:
        return APIServerError(message=message, status_code=400)

    return SimpleResponse(
        body={
            "message": message,
        },
        status_code=200,
    )

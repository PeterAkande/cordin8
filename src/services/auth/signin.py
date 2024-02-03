import json
import logging
import traceback

from proxy_response_handler.api_exception import APIServerError
from proxy_response_handler.simple_response import SimpleResponse
from decorators.authentication_n_authorizer_decorator import cordin8_api
from utils.cognito_utils import Cordin8CognitoHandler
from utils.dynamo_db_handlers.user_db_handler import UserDynamoDbHandler


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cordin8_api(authorized=False)
def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)

    email = body.get("email", None)
    password = body.get("password", None)

    if email is None or password is None:
        return APIServerError("Password or Email not present", status_code=400)

    cognito_handler = Cordin8CognitoHandler()
    user_dynamodb_handler = UserDynamoDbHandler()

    user_found, user_token = cognito_handler.sign_in_org_or_user(
        email=email, password=password
    )

    if not user_found:
        return APIServerError("Password or Email not present", status_code=400)

    access_token = user_token["AuthenticationResult"]["AccessToken"]
    refresh_token = user_token["AuthenticationResult"]["RefreshToken"]

    (
        operation_success,
        error_message,
        email_verified,
        user_id,
        profile_type,
    ) = cognito_handler.get_user_details_from_cognito(email=email)

    if not operation_success:
        return APIServerError(error_message, status_code=400)

    if not email_verified:
        return APIServerError(
            "User is not verified. Please verify user", status_code=400
        )

    logger.info(f"The profile type is {profile_type}")

    if profile_type == "user":

        user = user_dynamodb_handler.get_user_with_id(id=user_id)

        if user is None:
            return APIServerError("User not found", status_code=400)

        body = {
            "message": "Sign in Succesful",
            "data": {
                "auth_tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "user": user.model_dump(),
            },
        }
        logger.info(f"The body is {body}")

        return SimpleResponse(body=body, status_code=200)

    body = {
        "message": "Sign in Succesful",
        "data": {
            "auth_tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            "org": "Org details incoming",
        },
    }
    return SimpleResponse(body=body, status_code=200)

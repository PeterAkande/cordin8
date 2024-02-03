import datetime
import json
import logging
import traceback

from pydantic import ValidationError

from proxy_response_handler.api_exception import APIServerError
from models.user import UserSignUp, User
from proxy_response_handler.simple_response import SimpleResponse
from decorators.authentication_n_authorizer_decorator import cordin8_api
from utils.cognito_utils import Cordin8CognitoHandler
from utils.dynamo_db_handlers.user_db_handler import (
    UserDynamoDbHandler,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cordin8_api(authorized=False)
def lambda_handler(event, context, access_token=None):

    logger.info("event")
    logger.info(event)

    print("Event Print")
    print(event)

    try:
        body = json.loads(event.get("body", {}))
    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)
    try:
        user_sign_up_model = UserSignUp(**body)
    except ValidationError as e:
        traceback.print_exc()
        return APIServerError("Bad Request, Cant parse body", status_code=400)

    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)

    cognito_handler = Cordin8CognitoHandler()
    user_dynamodb_handler = UserDynamoDbHandler()

    signed_up, error = cognito_handler.sign_up_user(user=user_sign_up_model)

    if not signed_up:
        logger.info(f"Error signing up is {error}")
        return APIServerError(error, status_code=400)
    (
        operation_successful,
        error_message,
        email_verified,
        user_id,
        profile_type,
    ) = cognito_handler.get_user_details_from_cognito(email=user_sign_up_model.email)

    if not operation_successful:
        return APIServerError(error_message, status_code=400)

    date_created = datetime.datetime.now().isoformat()
    user_details = {
        **user_sign_up_model.model_dump(),
        "user_id": user_id,
        "date_created": date_created,
        "is_verified": False,
    }

    logger.info(f"User Details ot be parses is: {user_details}")
    try:
        user = User(**user_details)
    except ValidationError as e:
        traceback.print_exc()
        logger.info(f"Validation error, {e}")
        return APIServerError("An Error occurred", status_code=500)

    except Exception as e:
        traceback.print_exc()

        return APIServerError("An Error occurred", status_code=500)

    saved_successfully = user_dynamodb_handler.save_user_details(user)
    # saved_successfully = True

    if not saved_successfully:
        return APIServerError("An Unknown Error occurred", status_code=500)

    return SimpleResponse(
        body={
            "message": "User Registered, check email for verification code",
            "user": user.model_dump(),
        },
        status_code=200,
    )

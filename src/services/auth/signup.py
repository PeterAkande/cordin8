import json
import logging
import traceback

from pydantic import ValidationError

from src.proxy_response_handler.api_exception import APIServerError
from src.models.user import UserSignUp, User
from src.proxy_response_handler.simple_response import SimpleResponse
from src.utils.cognito_utils import Cordin8CognitoHandler
from src.utils.dynamo_db_handlers.user_db_handler import save_user_details

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context, access_token=None):
    try:
        body = json.loads(event["body"])
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

    cognito_handler.sign_up_user(user=user_sign_up_model)
    (
        email_verified,
        user_id,
        phone_verified,
    ) = cognito_handler.get_user_details_from_cognito(email=user_sign_up_model.email)

    if user_id is None:
        return APIServerError("An Error occurred", status_code=400)

    user_details = {**user_sign_up_model.model_dump_json(), "user_id": user_id}
    user = User(**user_details)
    save_user_details(user)

    return SimpleResponse(
        body={"message": "User Registered", "user": user.model_dump_json()},
        status_code=200,
    )

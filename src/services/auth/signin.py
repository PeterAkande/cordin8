import json
import traceback

from proxy_response_handler.api_exception import APIServerError
from proxy_response_handler.simple_response import SimpleResponse
from decorators.authentication_n_authorizer_decorator import cordin8_api
from utils.cognito_utils import Cordin8CognitoHandler
from utils.dynamo_db_handlers.user_db_handler import UserDynamoDbHandler

@cordin8_api()
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

    user_found, user_token = Cordin8CognitoHandler().sign_in_org_or_user(
        email=email, password=password
    )

    if not user_found:
        return APIServerError("Password or Email not present", status_code=400)

    # profile_type = user.get("profile_type", None)

    # if profile_type is None:
    #     return APIServerError("User not found", status_code=400)

    # user = get_user_with_email(email=email)

    # if user is None:
    #     return APIServerError("User not found", status_code=404)

    body = {"access_tokens": user_token}

    return SimpleResponse(body=body, status_code=200)

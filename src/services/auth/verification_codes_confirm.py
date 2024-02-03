import json
import traceback
from decorators.authentication_n_authorizer_decorator import cordin8_api
from proxy_response_handler.api_exception import APIServerError
from proxy_response_handler.simple_response import SimpleResponse
from utils.dynamo_db_handlers.user_db_handler import UserDynamoDbHandler
from utils.cognito_utils import Cordin8CognitoHandler


@cordin8_api(authorized=False)
def lambda_handler(event, context, access_token=None):
    """
    This would handle verifying the access token of the user.
    A POST request would mean that the user is to be verified.
    """

    try:
        body = json.loads(event.get("body", {}))
    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)

    cognito_handler = Cordin8CognitoHandler()
    user_dynamodb_handler = UserDynamoDbHandler()

    # Get the email and the code from the body
    email = body.get("email", None)
    code = body.get("code", None)

    if email is None or code is None:
        return APIServerError("Bad request, Code or email not given", status_code=400)

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

    # Now check if the code entered was valids
    success, message = cognito_handler.verify_user_code(code=code, email=email)

    if not success:
        return APIServerError(message=message, status_code=400)

    user = user_dynamodb_handler.get_user_with_id(user_id)
    user.is_verified = True

    # Save the new user details
    user_dynamodb_handler.save_user_details(user)

    return SimpleResponse(body={"message": "User verified successfully"})

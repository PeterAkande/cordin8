import json
import traceback
from decorators.authentication_n_authorizer_decorator import cordin8_api
from proxy_response_handler.api_exception import APIServerError


@cordin8_api()
def lambda_handler(event, context, access_token=None):
    """
    This would handle verifying the access token of the user.
    A GET request would mean that a verification code is needed.
    A POST request would mean that the user is to be verified.
    """

    try:
        body = json.loads(event.get("body", {}))
    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)

    # Get the email and the id of the user

    pass

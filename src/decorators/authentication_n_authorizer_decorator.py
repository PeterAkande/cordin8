import traceback

from src.proxy_response_handler.api_exception import APIServerError
from src.proxy_response_handler.lambda_proxy_response import LambdaProxyResponse
from src.utils.cognito_utils import Cordin8CognitoHandler


def cordin8_api(authorized: bool = True):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                event, context = args

                if authorized:

                    token_payload = event['headers']['Authorization']

                    if token_payload is None:
                        raise APIServerError("Please pass the token in the Authorization header", status_code=400)

                    user_details, token = Cordin8CognitoHandler().validate_user_token(token_payload)
                    response = f(*args, **kwargs, user_details=user_details, access_token=token)

                else:
                    response = f(*args, **kwargs)

                # The payload returned must be a lambda response
                if isinstance(response, LambdaProxyResponse):
                    api_res = response.generate_response()
                    return api_res
                else:
                    raise APIServerError('Response is not a valid LambdaProxyResponse', 500)
            except APIServerError as e:
                traceback.print_exc()
                traceback.format_exc()
                return e.generate_response()

            except Exception as e:
                traceback.print_exc()
                traceback.format_exc()
                return APIServerError(f'[{type(e)}] Unknown Error: {e}', 500, inner=e).generate_response()

        return wrapper

    return decorator

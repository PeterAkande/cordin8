import traceback

from src.proxy_response_handler.api_exception import APIServerError
from src.proxy_response_handler.lambda_proxy_response import LambdaProxyResponse


def cordin8_api(authorized: bool = True):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                event, context = args

                if authorized:

                    user_details, token = token_utilities.validate_token(event)
                    response = f(*args, **kwargs, user_details=user_details, access_token=token)
                else:
                    response = f(*args, **kwargs)

                # Enforce the LambdaProxyResponse
                if isinstance(response, LambdaProxyResponse):
                    api_res = response.generate_response()
                    return api_res
                else:
                    raise APIServerError('Response is not a valid LambdaProxyResponse', 500)
            except APIServerError as e:
                traceback.print_exc()
                tb = traceback.format_exc()
                return e.generate_response()
            except Exception as e:
                traceback.print_exc()
                tb = traceback.format_exc()
                return APIServerError(f'[{type(e)}] Unknown Error: {e}', 500, inner=e).generate_response()

        return wrapper

    return decorator

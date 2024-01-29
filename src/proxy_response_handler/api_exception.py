from src.proxy_response_handler.lambda_proxy_response import LambdaProxyResponse


class APIServerError(Exception, LambdaProxyResponse):
    DEFAULT_CLIENT_MESSAGE = {
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        500: 'Internal Server Error',
        501: 'Not Implemented'
    }

    def __init__(self, message: str, status_code: int = 400, inner: Exception = None,
                 client_message: str = None):
        self.message = message
        self.status_code = status_code
        self.inner = inner

        if client_message:
            self.client_message = client_message
        else:
            self.client_message = self.DEFAULT_CLIENT_MESSAGE.get(status_code, 'Unknown Error')

        Exception.__init__(self, message)
        LambdaProxyResponse.__init__(
            self,
            body={
                'message': self.message
            },
            status_code=self.status_code
        )

        print(f'[API_SERVER_ERROR] ({status_code}) {message} (Client Message: {self.client_message})')

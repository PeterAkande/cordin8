from src.proxy_response_handler.lambda_proxy_response import LambdaProxyResponse


class SimpleResponse(LambdaProxyResponse):
    def __init__(self, body, status_code=200):
        super().__init__(body, status_code)

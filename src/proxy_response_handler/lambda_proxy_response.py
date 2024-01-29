import decimal
import json
from typing import Union, Dict


class _DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(_DecimalEncoder, self).default(o)


class LambdaProxyResponse:
    """
    This class formats the body the way it API Gateway expects it
    https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format
    """

    def __init__(self, body: Union[str, dict], status_code: int, headers: Union[None, Dict] = None,
                 multi_value_headers: Union[None, Dict] = None,
                 is_base64_encoded: bool = False, **kwargs):
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.multi_value_headers = multi_value_headers
        self.is_base64_encoded = is_base64_encoded

    def generate_response(self):
        headers = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET, PUT, DELETE, HEAD"
        }
        if self.headers:
            headers = {**headers, **self.headers}

        return {
            'statusCode': self.status_code,
            'body': self.body if isinstance(self.body, str) else json.dumps(self.body, cls=_DecimalEncoder),
            'headers': headers,
            'multiValueHeaders': self.multi_value_headers,
            'isBase64Encoded': self.is_base64_encoded
        }

import json

def lambda_handler(event, context):
    """
    Handler.
    """

    print("This was invojedddd???")

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps({"hello": "World!"}),
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
    }

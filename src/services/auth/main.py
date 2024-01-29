import json

def lambda_handler(event, context):
    """
    User
    """

    print("This was Not???")

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps({"hello": "New World!"}),
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
    }

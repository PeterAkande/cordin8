import traceback

import boto3
from typing import Optional

from botocore.exceptions import ClientError

from src.models.user import User
from src.constants import user_table_name


def save_user_details(user: User) -> bool:
    dynamodb_resource = boto3.resource('dynamodb')
    users_table = dynamodb_resource.Table(user_table_name)

    try:
        response = users_table.put_item(Item=user.model_dump_json())
    except ClientError as err:
        return False
        pass

    except Exception as e:
        traceback.print_exc()
        return False

    return True


def get_user_with_email(email: str) -> Optional[User]:
    dynamodb_resource = boto3.resource('dynamodb')
    users_table = dynamodb_resource.Table(user_table_name)

    try:
        response = users_table.scan(
            FilterExpression="email = :email_address",
            ExpressionAttributeValues={
                ":email_address": email
            }
        )

        if "Items" in response:
            user_details = response['Items']

            user = User(**user_details)

            return user

    except ClientError as err:
        return None

    return None

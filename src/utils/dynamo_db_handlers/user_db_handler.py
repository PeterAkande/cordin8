import logging
import traceback

import boto3
from typing import Optional

from botocore.exceptions import ClientError

from models.user import User
from constants import user_table_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def save_user_details(user: User) -> bool:
    logger.info('User details to be saved')
    logger.info(f'{user.model_dump()}')

    logger.info(f'Table name is {user_table_name}')
    dynamodb_resource = boto3.resource('dynamodb')
    users_table = dynamodb_resource.Table(user_table_name)

    logger.info("User details os")

    try:
        response = users_table.put_item(Item=user.model_dump())
        logger.info('Saved Successfully')
    except ClientError as err:
        logger.info(f"Eeror saving details, {err.response['Error']} ")
        return False

    except Exception as e:
        logger.info(f'Saved Error {e}')
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

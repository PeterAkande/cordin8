import logging
import traceback

import boto3
from typing import Optional

from botocore.exceptions import ClientError
from pydantic import ValidationError

from models.user import User
from constants import user_table_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class UserDynamoDbHandler:

    def __init__(self) -> None:
        self.dynamodb_resource = boto3.resource("dynamodb")
        self.users_table = self.dynamodb_resource.Table(user_table_name)
        pass

    def save_user_details(self, user: User) -> bool:
        logger.info("User details to be saved")
        logger.info(f"{user.model_dump()}")

        logger.info(f"Table name is {user_table_name}")

        logger.info("User details os")

        try:
            response = self.users_table.put_item(Item=user.model_dump())
            logger.info("Saved Successfully")
        except ClientError as err:
            logger.info(f"Eeror saving details, {err.response['Error']} ")
            return False

        except Exception as e:
            logger.info(f"Saved Error {e}")
            traceback.print_exc()
            return False

        return True

    def get_user_with_email(self, email: str) -> Optional[User]:
        """
        Get a user with an email.
        Dont use this!. It makes a scan which can be computationaly intensive.

        Instead, get the id of the user from cognito and search by the id instead

        """

        try:
            response = self.users_table.scan(
                FilterExpression="email = :email_address",
                ExpressionAttributeValues={":email_address": email},
            )

            if "Items" in response:
                user_details = response["Items"]

                user = User(**user_details)

                return user

        except ClientError as err:
            return None

        return None
    
    def get_user_with_id(self, id: str) -> Optional[User]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
        """

        logger.info(f"Checking for user with Id: {id}")

        try:
            response = self.users_table.get_item(Key={"user_id": id})
            logger.info(f"Response is {response}")

            user_details = response["Item"]

            if user_details is None:
                return None

            logger.info(f"Gotten user details, {user_details}")
            logger.info(f"User type {type(user_details)}")

            # user = User(name="perer", user_id="Peuod", )
            
            user = User(**user_details)

            logger.info(f"Parsed User as {user}")
            return user

        except ClientError as err:
            traceback.print_exc()

            logger.error(f"Error is {err.response['Errror']['Message']}")
            return None

        except ValidationError as ve:
            logger.error(f"Error is {ve}")
            return None

        except Exception as e:
            traceback.print_exc()

            logger.error(f"Error is {e}")
            return None

        return None

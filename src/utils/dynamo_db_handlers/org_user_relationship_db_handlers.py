import logging
import traceback

import boto3
from typing import Optional

from botocore.exceptions import ClientError
from pydantic import ValidationError

from models.organization import Organization
from constants import orgs_user_table

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class OrgAndMemberdDynamoDbHandler:
    """
    This would handle all that has to do with an organization and its members
    """

    def __init__(self) -> None:
        self.dynamodb_resource = boto3.resource("dynamodb")
        self.org_n_members_table = self.dynamodb_resource.Table(orgs_user_table)
        pass

    def save_org_details(self, org: Organization) -> bool:
        logger.info("Org details to be saved")
        logger.info(f"{org.model_dump()}")

        logger.info(f"Table name is {org_table_name}")

        try:
            response = self.org_table.put_item(Item=org.model_dump())
            logger.info("Saved Successfully")
        except ClientError as err:
            logger.info(f"Error saving details, {err.response['Error']} ")
            return False

        except Exception as e:
            logger.info(f"Saved Error {e}")
            traceback.print_exc()
            return False

        return Tr

    def get_org_with_email(self, email: str) -> Optional[Organization]:
        """
        Get a org with an email.
        Dont use this!. It makes a scan which can be computationaly intensive.

        Instead, get the id of the org from cognito and search by the id instead

        """

        try:
            response = self.org_table.scan(
                FilterExpression="email = :email_address",
                ExpressionAttributeValues={":email_address": email},
            )

            if "Items" in response and len(response["Items"]) > 0:
                org_details = response["Items"][0]

                org = Organization(**org_details)

                return org

        except ClientError as err:
            return None

        return None

    def get_org_with_id(self, id: str) -> Optional[Organization]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
        """

        logger.info(f"Checking for Organization with Id: {id}")

        try:
            response = self.org_table.get_item(Key={"org_id": id})
            logger.info(f"Response is {response}")

            org_details = response["Item"]

            if org_details is None:
                return None

            logger.info(f"Gotten org details, {org_details}")

            org = Organization(**org_details)

            logger.info(f"Parsed Org as {org}")
            return org

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

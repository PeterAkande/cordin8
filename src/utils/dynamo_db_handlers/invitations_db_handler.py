import datetime
import logging
import traceback
from typing import List, Optional
import boto3
from pydantic import TypeAdapter, ValidationError

from constants import invitations_table
from models.invitation import Invitation
from botocore.exceptions import ClientError

from proxy_response_handler.api_exception import APIServerError
from boto3.dynamodb.conditions import Key


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class InvitationsDbHandler:

    def __init__(self) -> None:
        self.dynamodb_resource = boto3.resource("dynamodb")
        self.invitations_table = self.dynamodb_resource.Table(invitations_table)
        pass

    def create_invitations(self, user_email: str, org_id: str) -> bool:
        logger.info("User details to be saved")

        date_created = datetime.datetime.now().isoformat()
        invitation = Invitation(
            user_email=user_email,
            org_id=org_id,
            date_accepted="",
            date_invited=date_created,
            accepted=False,
        )

        logger.info(f"{invitation.model_dump()}")

        try:
            response = self.invitations_table.put_item(Item=invitation.model_dump())
            logger.info("Saved Successfully")
        except ClientError as err:
            logger.info(f"Eeror saving Invitation, {err.response['Error']} ")
            return False

        except Exception as e:
            logger.info(f"Saved Error {e}")
            traceback.print_exc()
            return False

        return True

    def get_invitations_for_user(self, user_email: str) -> List[Invitation]:
        """
        Get a user with an email.
        Dont use this!. It makes a scan which can be computationaly intensive.

        Instead, get the id of the user from cognito and search by the id instead
        """

        try:
            response = self.invitations_table.scan(
                FilterExpression="user_email = :user_email",
                ExpressionAttributeValues={":user_email": user_email},
            )

            if "Items" in response:
                invitations_details = response["Items"]

                invitations_adapter = TypeAdapter(List[Invitation])
                invitations = invitations_adapter.validate_python(invitations_details)

                logger.info(
                    f"Gotten invitations_details details, {invitations_details}"
                )

                logger.info(f"Parsed Invitations as {invitations}")

                return invitations

            return []

        except ClientError as err:
            traceback.print_exc()

            logger.error(f"Error is {err.response['Errror']['Message']}")
            raise APIServerError(
                f"An error occurred {err.response['Errror']['Message']}",
                status_code=500,
            )

        except ValidationError as ve:
            logger.error(f"Error is {ve}")
            raise APIServerError(
                f"Error reading data",
                status_code=500,
            )

        except Exception as e:
            traceback.print_exc()

            logger.error(f"Error is {e}")
            raise APIServerError(
                f"An error occurred",
                status_code=500,
            )

        return []

    def get_invitations_for_org(self, org_id: str) -> List[Invitation]:

        logger.info(f"Checking invitations for organization with id: {org_id}")

        try:
            response = self.invitations_table.query(
                KeyConditionExpression=Key("org_id").eq(org_id)
            )
            logger.info(f"Response is {response}")

            invitations_details = response.get("Items", None)

            if invitations_details is None:
                return None

            invitations_adapter = TypeAdapter(List[Invitation])
            invitations = invitations_adapter.validate_python(invitations_details)

            logger.info(f"Gotten invitations_details details, {invitations_details}")

            logger.info(f"Parsed Invitations as {invitations}")
            return invitations

        except ClientError as err:
            traceback.print_exc()

            logger.error(f"Error is {err.response['Errror']['Message']}")
            raise APIServerError(
                f"An error occurred {err.response['Errror']['Message']}",
                status_code=500,
            )

        except ValidationError as ve:
            logger.error(f"Error is {ve}")
            raise APIServerError(
                f"Error reading data",
                status_code=500,
            )

        except Exception as e:
            traceback.print_exc()

            logger.error(f"Error is {e}")
            raise APIServerError(
                f"An error occurred",
                status_code=500,
            )

    def get_invitation_details(
        self, user_email: str, org_id: str
    ) -> Optional[Invitation]:
        """
        This gets the invitation details for a user and an org

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
        """

        try:
            response = self.invitations_table.get_item(
                Key={"org_id": org_id, "user_email": user_email}
            )
            logger.info(f"Response is {response}")

            invitation_details = response["Item"]

            if invitation_details is None:
                return None

            logger.info(f"Gotten invitation_details details, {invitation_details}")

            invitation = Invitation(**invitation_details)

            logger.info(f"Parsed Invitation is {invitation}")

            return invitation

        except ClientError as err:
            traceback.print_exc()

            logger.error(f"Error is {err.response['Errror']['Message']}")
            return []

        except ValidationError as ve:
            logger.error(f"Error is {ve}")
            return []

        except Exception as e:
            traceback.print_exc()

            logger.error(f"Error is {e}")
            return None

    def delete_invitation_details(self, user_email: str, org_id: str) -> bool:
        """
        This deletes the invitation details for a user and an org

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
        """

        try:
            response = self.invitations_table.delete_item(
                Key={
                    "org_id": org_id,
                    "user_email": user_email,
                }
            )

            return True

        except ClientError as err:
            traceback.print_exc()

            logger.error(f"Error is {err.response['Errror']['Message']}")
            raise APIServerError(
                f"{err.response['Errror']['Message']}", status_code=500
            )

        except ValidationError as ve:
            logger.error(f"Error is {ve}")

            raise APIServerError(
                f"{err.response['Errror']['Message']}", status_code=500
            )

        except Exception as e:
            traceback.print_exc()

            logger.error(f"Error is {e}")
            raise APIServerError(f"An error occurred", status_code=500)

        return False

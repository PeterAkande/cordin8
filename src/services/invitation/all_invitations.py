import json
import logging
import traceback

from decorators.authentication_n_authorizer_decorator import cordin8_api
from proxy_response_handler.api_exception import APIServerError

from proxy_response_handler.simple_response import SimpleResponse
from utils.dynamo_db_handlers.invitations_db_handler import InvitationsDbHandler
from utils.dynamo_db_handlers.user_db_handler import UserDynamoDbHandler
from utils.dynamo_db_handlers.org_db_handler import OrgDynamoDbHandler


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cordin8_api(authorized=True)
def lambda_handler(event, context, user_details=None, access_token=None):
    """
    This function would handle getting all the invitations for a user or for an organization
    """

    logger.info(f"This is the user details {user_details}")

    profile_type = user_details.get("profile_type", None)

    if profile_type is None:
        raise APIServerError("Invalid user, cant get details of user", status_code=400)

    profile_id = user_details.get("profile_id", None)

    logger.info(f"The profile type is {profile_type} and id is {profile_id}")

    user_db_handler = UserDynamoDbHandler()
    invitations_db_handler = InvitationsDbHandler()
    org_db_handler = OrgDynamoDbHandler()

    if profile_type == "user":

        logger.info("Getting user info")
        user_details = user_db_handler.get_user_with_id(id=profile_id)
        logger.info(f"Gotten user info: {user_details}")

        if user_details is None:
            raise APIServerError(
                f"User with Id {profile_id} not found", status_code=400
            )

        invitations = invitations_db_handler.get_invitations_for_user(
            user_email=user_details.email
        )

        new_parsed_invitations = []

        for invitation in invitations:
            org_details = org_db_handler.get_org_with_id(id=invitation.org_id)

            invitation_details = invitation.model_dump()

            if org_details is None:
                invitation_details["org"] = None
            else:
                invitation_details["org"] = org_details.model_dump()

            new_parsed_invitations.append(invitation_details)

        return SimpleResponse(
            body={"invitations": new_parsed_invitations},
            status_code=200,
        )

    elif profile_type == "org":

        invitations = invitations_db_handler.get_invitations_for_org(org_id=profile_id)

        return SimpleResponse(
            body={
                "invitations": [invitation.model_dump() for invitation in invitations]
            },
            status_code=200,
        )

    else:
        raise APIServerError("Invalid user type", status_code=400)

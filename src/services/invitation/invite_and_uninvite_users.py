import json
import traceback
from decorators.authentication_n_authorizer_decorator import cordin8_api

import logging

from proxy_response_handler.simple_response import SimpleResponse
from proxy_response_handler.api_exception import APIServerError
from models.invitation import Invitation
from utils.dynamo_db_handlers.invitations_db_handler import InvitationsDbHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cordin8_api(authorized=True)
def lambda_handler(event, context, user_details=None, access_token=None):
    """
    This function would handle inviting and uninvite a user to an organization.

    For now, this action can be performed only by an organization.
    """

    logger.info(f"This is the user details {user_details}")
    logger.info(f"This is the Event  {event}")

    profile_type = user_details.get("profile_type", None)

    if profile_type != "org":
        APIServerError(
            "Only organizations can invite and uninvite users", status_code=400
        )

    org_id = user_details.get("profile_id", None)

    if org_id is None:
        APIServerError("Only organizations can invite users", status_code=400)

    try:
        body = json.loads(event["body"])
        http_method = event["httpMethod"]
    except Exception as e:
        traceback.print_exc()

        raise APIServerError("Bad Request, Cant parse body", status_code=400)

    user_email = body.get("user_email", None)

    if user_email is None:
        # Bad Request
        raise APIServerError(
            "Please give the user email to be invited", status_code=400
        )

    invitation_db_handler = InvitationsDbHandler()

    if http_method == "POST":

        operation_successful = invitation_db_handler.create_invitations(
            user_email=user_email, org_id=org_id
        )

        if not operation_successful:
            response = SimpleResponse(
                body={"messsage": "Couldnt send invitations"}, status_code=400
            )
        else:
            response = SimpleResponse(
                body={"message": f"Invitation sent to {user_email}"}
            )
    elif http_method == "DELETE":
        operation_successful = invitation_db_handler.delete_invitation_details(
            user_email=user_email, org_id=org_id
        )

        if not operation_successful:
            response = SimpleResponse(
                body={"messsage": "Couldnt delete invitation"}, status_code=400
            )
        else:
            response = SimpleResponse(
                body={"message": f"Invitation sent to {user_email} deleted"}
            )

    else:
        raise APIServerError(f"{http_method} not supported", status_code=404)

    return response


def _uninvite_user(user_email: str, org_id: str) -> bool:
    """
    This would handle uninviting a user
    """

    pass

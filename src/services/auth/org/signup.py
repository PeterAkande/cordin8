import datetime
import json
import logging
import traceback

from pydantic import ValidationError

from decorators.authentication_n_authorizer_decorator import cordin8_api
from models.organization import OrganizationSignUp, Organization
from proxy_response_handler.api_exception import APIServerError
from proxy_response_handler.simple_response import SimpleResponse
from utils.cognito_utils import Cordin8CognitoHandler
from utils.dynamo_db_handlers.org_db_handler import OrgDynamoDbHandler


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cordin8_api(authorized=False)
def lambda_handler(event, context, access_token=None):

    logger.info("event")
    logger.info(event)

    try:
        body = json.loads(event.get("body", {}))
    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)
    try:
        org_signup_model = OrganizationSignUp(**body)
    except ValidationError as e:
        traceback.print_exc()
        return APIServerError("Bad Request, Cant parse body", status_code=400)

    except Exception as e:
        traceback.print_exc()

        return APIServerError("Bad Request, Cant parse body", status_code=400)

    cognito_handler = Cordin8CognitoHandler()
    org_dynamodb_handler = OrgDynamoDbHandler()

    signed_up, error = cognito_handler.sign_up_org(org=org_signup_model)

    if not signed_up:
        logger.info(f"Error signing up is {error}")
        return APIServerError(error, status_code=400)
    (
        operation_successful,
        error_message,
        email_verified,
        org_id,
        profile_type,
    ) = cognito_handler.get_user_details_from_cognito(email=org_signup_model.email)

    if not operation_successful:
        return APIServerError(error_message, status_code=400)

    date_created = datetime.datetime.now().isoformat()
    org_details = {
        **org_signup_model.model_dump(),
        "org_id": org_id,
        "date_created": date_created,
        "is_verified": False,
    }

    logger.info(f"Organization Details ot be parses is: {org_details}")
    try:
        org = Organization(**org_details)
    except ValidationError as e:
        traceback.print_exc()
        logger.info(f"Validation error, {e}")
        return APIServerError("An Error occurred", status_code=500)

    except Exception as e:
        traceback.print_exc()

        return APIServerError("An Error occurred", status_code=500)

    saved_successfully = org_dynamodb_handler.save_org_details(org)

    if not saved_successfully:
        return APIServerError("An Unknown Error occurred", status_code=500)

    return SimpleResponse(
        body={
            "message": "Orgaanization Registered, check email for verification code",
            "user": org.model_dump(),
        },
        status_code=200,
    )

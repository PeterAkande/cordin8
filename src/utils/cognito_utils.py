import base64
import hashlib
import hmac
import logging
import traceback

import boto3
import jwt
from botocore.exceptions import ClientError

from constants import user_pool_id, client_id, client_secret, region
from models.user import UserSignUp
from models.organization import OrganizationSignUp
from proxy_response_handler.api_exception import APIServerError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Cordin8CognitoHandler:
    """
    This would handle Authentication for the Cordin8 service
    """

    def __init__(self):
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client_secret = client_secret

        self.cognito_idp_client = boto3.client("cognito-idp")

    def sign_up_user(self, user: UserSignUp) -> (bool, str):
        """
        Sign up a user
        """
        try:

            user_phone = str(user.phone).replace("tel:", "").replace("-", "")
            kwargs = {
                "ClientId": self.client_id,
                "Username": user.email,
                "Password": user.password,
                "UserAttributes": [
                    {"Name": "email", "Value": user.email},
                    {"Name": "name", "Value": user.name},
                    {"Name": "phone_number", "Value": user_phone},
                    {"Name": "custom:profile_type", "Value": "user"},
                ],
            }

            print(f"The params is {kwargs}")
            if self.client_secret is not None:
                kwargs["SecretHash"] = self._get_secret_hash_for_user(user.email)
            response = self.cognito_idp_client.sign_up(**kwargs)

        except ClientError as err:
            logger.info(f'Error Signing up is given by {err.response["Error"]}')
            print(f"Error is {err.response['Error']}")

            return False, err.response["Error"]["Message"]

        return True, "Success"

    def sign_up_org(self, org: OrganizationSignUp) -> (bool, str):
        """
        Sign up an org
        """
        try:
            kwargs = {
                "ClientId": self.client_id,
                "Username": org.email,
                "Password": org.password,
                "UserAttributes": [
                    {"Name": "email", "Value": org.email},
                    {"Name": "name", "Value": org.name},
                    {"Name": "custom:profile_type", "Value": "org"},
                ],
            }
            if self.client_secret is not None:
                kwargs["SecretHash"] = self._get_secret_hash_for_user(org.email)
            response = self.cognito_idp_client.sign_up(**kwargs)

        except ClientError as err:

            return False, err.response["Error"]["Code"]

        return True, "Success"

    def sign_in_org_or_user(self, email: str, password: str) -> (bool, dict):
        """
        This would sign in a user
        It would get the access token of the user
        """

        try:
            kwargs = {
                "UserPoolId": self.user_pool_id,
                "ClientId": self.client_id,
                "AuthFlow": "ADMIN_USER_PASSWORD_AUTH",
                "AuthParameters": {"USERNAME": email, "PASSWORD": password},
            }
            if self.client_secret is not None:
                kwargs["AuthParameters"]["SECRET_HASH"] = (
                    self._get_secret_hash_for_user(email)
                )

            response = self.cognito_idp_client.admin_initiate_auth(**kwargs)

        except ClientError as err:
            return False, {}

        return True, response

    def get_user_details_from_cognito(self, email: str) -> (bool, str, bool, str):
        """
        (bool, str, bool, str) => operation_success_status, error, email_verified, user_id
        """

        try:
            verify_response = self.cognito_idp_client.admin_get_user(
                UserPoolId=self.user_pool_id, Username=email
            )
        except ClientError as err:
            # if err.response["Error"]["Code"] == "UserNotFoundException":
            return False, err.response["Error"]["Message"], False, ""

        except Exception as e:
            traceback.print_exec()

            logger.info("An Errro occurred")
            return False, "An Error occurred", False, ""

        user_attributes = verify_response["UserAttributes"]

        email_verified = None
        user_id = None
        phone_verified = None
        for node in user_attributes:
            if node["Name"] == "email_verified":
                email_verified = node["Value"]
            elif node["Name"] == "sub":
                user_id = node["Value"]

        return email_verified, user_id

    def _get_secret_hash_for_user(self, email_address):
        msg = email_address + self.client_id
        digest = hmac.new(
            str(self.client_secret).encode("utf-8"),
            msg=str(msg).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        secret_hash = base64.b64encode(digest).decode()
        return secret_hash

    def validate_user_token(self, token: str):
        """
        Validate the token passed
        """

        if not token.startswith("Bearer "):
            raise APIServerError(
                'Invalid token format, token should start with "Bearer "', 401
            )

        try:
            user = self.cognito_idp_client.get_user(access_token=token)
        except jwt.DecodeError as e:
            raise APIServerError("Invalid JWT token", 401, inner=e)
        except jwt.ExpiredSignatureError as e:
            raise APIServerError("JWT Token is expired", 401, inner=e)
        except Exception as e:
            if "Access Token has expired" in str(e):
                raise APIServerError("JWT Token is expired", 401, inner=e)
            else:
                raise e

        return user, token

    def verify_user_code(self, code: str, email: str) -> (bool, str):
        """
        This would verify a user sign up with the code that was sent to the user
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/confirm_sign_up.html
        """

        try:
            secret_hash = self._get_secret_hash_for_user(email_address=email)

            response = self.cognito_idp_client.confirm_sign_up(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=email,
                ConfirmationCode=code,
            )
        except ClientError as err:
            logger.info("Error confirming Sign up")
            logger.info(err.response["Error"]["Message"])

            return False, err.response["Error"]["Message"]

        except Exception as e:
            logger.info("An unknown error occurred when confirming signing up")

            return False, "Unknown error occurred"

        return True, "User Confirmed successfully"

    def resend_verification_code(self, email: str) -> (bool, str):
        """
        This resends a verification code to this email address

        returns: (bool, str) => if the operation was successful, the error or some message
        """

        try:
            secret_hash = self._get_secret_hash_for_user(email_address=email)

            response = self.client_id.resend_confirmation_code(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=email,
            )
        except ClientError as err:
            logger.info("Error resending code")
            logger.info(err.response["Error"]["Message"])

            return False, err.response["Error"]["Message"]

        except Exception as e:
            logger.info("An unknown error occurred when resending codep")

            return False, "Unknown error occurred"

        return True, f"Code Sent to email {email} successfully"

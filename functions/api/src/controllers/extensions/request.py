from http import HTTPStatus

from common.exception.http_error import HTTPError
from fastapi import Request
from common.constants.error_codes import ErrorCodes
from common.constants.error_messages import ErrorMessages


class RequestExtension:
    """
    Extensions for HTTP requests.
    """

    def __init__(self, request: Request):
        """
        Initializes the RequestExtension instance.

        Args:
            request: The FastAPI Request object.
        """
        self.request = request

    def get_user_id(self) -> str:
        """
        Retrieves the user ID from the request context.

        Returns:
            The user ID if available, None otherwise.
        """
        try:
            return "883f885d-b56f-4382-b587-2d5b2b80f27f"
            user_id = self.request.scope["aws.event"]["requestContext"]["authorizer"][
                "lambda"
            ]["user_id"]
            return user_id
        except KeyError:
            raise HTTPError(
                HTTPStatus.UNAUTHORIZED,
                ErrorCodes.USER_NOT_FOUND,
                ErrorMessages.USER_NOT_FOUND_IN_REQUEST,
            )

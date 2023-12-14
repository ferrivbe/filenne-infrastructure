import json
from typing import Callable
from uuid import uuid4

from common.logger.handler import LoggerHandler
from fastapi import Request, Response, UploadFile
from fastapi.responses import JSONResponse
from utils.iterator import AsyncIteratorWrapper
from starlette.types import Message

from io import BytesIO


class RequestLoggingHandler:
    """
    A class for logging requests and responses in an ASGI application.

    :param service_name: A string representing the name of the service.
    :type service_name: str
    """

    def __init__(self, service_name: str):
        """
        Constructor method for RequestLoggingHandler.

        :param service_name: A string representing the name of the service.
        :type service_name: str
        """
        self._service_name = service_name

    async def set_body(self, request: Request):
        """
        A method to set the body of the request.

        :param request: An instance of the Request class representing the incoming request.
        :type request: Request
        """
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def log_request(self, request: Request, call_next: Callable):
        """
        A method to log the incoming request and outgoing response.

        :param request: An instance of the Request class representing the incoming request.
        :type request: Request
        :param call_next: A callable function to call the next middleware in the chain.
        :type call_next: Callable
        :returns: An instance of the Response class representing the response to the incoming request.
        :rtype: Response
        """
        request.state.request_id = str(uuid4())
        _logger = LoggerHandler(request, self._service_name)

        serialized_body: str = None

        if request.headers.get("content-type") is not None:
            content_type = request.headers.get("content-type").split(";")[0]

            if content_type != "multipart/form-data":
                await self.set_body(request)
                body = await request.body()
            else:
                body = {"test": "etst"}

            serialized_body = self._get_serialized_data(body)

        _logger.info(
            payload=serialized_body,
            message="client_received_request",
        )

        response: Response = await call_next(request)

        try:
            response_body = [
                section async for section in response.__dict__["body_iterator"]
            ]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(response_body))

            serialized_response_body = None
            if len(response_body) > 0:
                serialized_response_body = self._get_serialized_data(
                    response_body[0].decode()
                )

        except Exception as exception:
            serialized_response_body = {
                "errorCode": "InternalServerError",
                "message": "Something went wrong!",
                "detail": str(exception),
                "target": f"{request.method}|{request.url._url}",
            }

            _logger.exception(serialized_response_body)

            response = JSONResponse(serialized_response_body, status_code=500)

        response.headers["request_id"] = request.state.request_id

        _logger.info(
            payload=serialized_response_body,
            message="client_sent_response",
        )

        return response

    def _get_serialized_data(self, data) -> str:
        """
        Serializes data from a string to a Python object using JSON.

        :param data: The string representation of data to be deserialized.
        :type data: str
        :return: The deserialized Python object, or `None` if deserialization fails.
        :rtype: Union[None, Any]
        """
        try:
            if data:
                return json.loads(data)
            else:
                return None
        except:
            return None

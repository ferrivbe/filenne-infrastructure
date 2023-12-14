from common.exception.http_error import HTTPError
from controllers.health_controller import router as health_controller
from controllers.v1.file_controller import router as file_controller
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from mangum import Mangum
from middleware.exception import (
    default_exception_handler,
    exception_handler,
    python_exception_handler,
    request_validation_error_hanlder,
)
from middleware.request_logger import RequestLoggingHandler

service_name = "filenne-infrastructure"
app = FastAPI(title=service_name)

logger = RequestLoggingHandler(service_name=service_name)

# Add middleware first
app.middleware("http")(logger.log_request)

# Add handlers
app.add_exception_handler(HTTPError, exception_handler)
app.add_exception_handler(HTTPException, default_exception_handler)
app.add_exception_handler(Exception, python_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_hanlder)

# Add routers or include other routers
app.include_router(health_controller, prefix="/health")

handler = Mangum(app=app)

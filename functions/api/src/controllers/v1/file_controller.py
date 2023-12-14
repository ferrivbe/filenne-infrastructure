from http import HTTPStatus
from typing import List

from controllers.extensions.request import RequestExtension
from controllers.extensions.rules import Rules
from fastapi import APIRouter, Request, UploadFile
from models.file import (
    FileByPathDto,
    FileCreatedDto,
    FilesDeletedDto,
    FileSignedDto,
    FilesDto,
)
from models.http_error import HTTPErrorDto
from services.file_service import FileService

router = APIRouter()
service = FileService()
validator = Rules()


class FileController:
    """
    Th file controller.
    """

    def __init__(self):
        """
        Initializes a new instance of FileController class.
        """
        self.router = APIRouter()

    @router.post(
            "",
            tags=["File"],
            status_code=HTTPStatus.CREATED,
            responses={
                HTTPStatus.BAD_REQUEST: {"model": HTTPErrorDto},
                HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HTTPErrorDto},
            }
    )
    async def create_a_new_file(self, files: List[UploadFile], request: Request):
        """
        Creates a new file in filenne services.
        """


@router.post(
    "",
    tags=["File"],
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.CREATED: {"model": List[FileCreatedDto]},
        HTTPStatus.BAD_REQUEST: {"model": HTTPErrorDto},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HTTPErrorDto},
    },
    response_model_exclude_none=True,
)
async def create_new_file(
    files: List[UploadFile], request: Request, collection_id: str = None
):
    """
    Creates a new file.
    """
    request_handler = RequestExtension(request=request)

    for file in files:
        validator.match_filename_regex(file.filename)

    return service.create_file(
        files=files,
        collection_id=collection_id,
        user_id=request_handler.get_user_id(),
    )


@router.delete(
    "",
    tags=["File"],
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {"model": FilesDeletedDto},
        HTTPStatus.NOT_FOUND: {"model": HTTPErrorDto},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HTTPErrorDto},
    },
    response_model_exclude_none=True,
    response_model=FilesDeletedDto,
)
async def deletes_files_by_ids(files: FilesDto, request: Request):
    """
    Deletes a file by identifier.
    """
    request_handler = RequestExtension(request=request)

    return service.delete_files_by_id(
        user_id=request_handler.get_user_id(),
        files=files.files,
    )


@router.delete(
    "/{id}",
    tags=["File"],
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {"model": FilesDeletedDto},
        HTTPStatus.NOT_FOUND: {"model": HTTPErrorDto},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HTTPErrorDto},
    },
    response_model_exclude_none=True,
    response_model=FilesDeletedDto,
)
async def deletes_file_by_id(request: Request, id: str):
    """
    Deletes a file by identifier.
    """
    request_handler = RequestExtension(request=request)

    return service.delete_file_by_id(
        id=id,
        user_id=request_handler.get_user_id(),
    )


@router.get(
    "/{id}",
    tags=["File"],
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {"model": FileSignedDto},
        HTTPStatus.NOT_FOUND: {"model": HTTPErrorDto},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HTTPErrorDto},
    },
    response_model_exclude_none=True,
    response_model=FileSignedDto,
)
async def gets_file_by_id(request: Request, id: str):
    """
    Gets a file by identifier.
    """
    request_handler = RequestExtension(request=request)

    return service.get_file_by_id(
        user_id=request_handler.get_user_id(),
        id=id,
    )


@router.get(
    "",
    tags=["File"],
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {"model": FileByPathDto},
        HTTPStatus.NOT_FOUND: {"model": HTTPErrorDto},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HTTPErrorDto},
    },
    response_model=FileByPathDto,
    response_model_exclude_none=True,
)
async def gets_files_by_path(request: Request, path: str):
    """
    Gets files by path.
    """
    request_handler = RequestExtension(request=request)

    return FileByPathDto(
        path=path,
        files=service.get_files_by_path(
            user_id=request_handler.get_user_id(),
            path=path,
        ),
    )

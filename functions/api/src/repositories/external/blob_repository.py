import boto3
from common.constants.service_constants import ServiceConstants
from enum import Enum
from common.constants.repository_contants import RepositoryConstants


class RequestAction(str, Enum):
    """
    The request action enum.
    """

    GET_OBJECT = RepositoryConstants.REQUEST_GET_OBJECT
    """
    Get object request action enum member.
    """

    PUT_OBJECT = RepositoryConstants.REQUEST_PUT_OBJECT
    """
    Put object request action enum member.
    """


class BlobRespitory:
    """
    A class for working with an S3 blob repository.
    """

    def __init__(self):
        """
        Initializes a new instance of BlobRespitory class.
        """
        self.client = boto3.client(ServiceConstants.S3_CLIENT_NAME)

    def create_get_action_presigned_request(
        self,
        bucket_name: str,
        file_name: str,
        service_base_url: str,
        expires_in: int = 300,
    ):
        """
        Creates a presigned URL for an S3 bucket object.

        Args:
            bucket_name (str): The target bucket name.
            file_name (str): The file name.
            service_base_url (str): The service base URL.
            expires_in (int): The expiration time for the presigned url.
        """
        url: str = self._create_presigned_request(
            bucket_name=bucket_name,
            action=RequestAction.GET_OBJECT,
            file_name=file_name,
            expires_in=expires_in,
        )
        return url.replace(
            bucket_name + RepositoryConstants.AWS_S3_BUCKET_DOMAIN_SUFFIX,
            service_base_url,
        )

    def create_put_action_presigned_request(
        self,
        bucket_name: str,
        file_name: str,
        expires_in: int = 300,
    ):
        """
        Creates a presigned URL for an S3 bucket object.

        Args:
            bucket_name (str): The target bucket name.
            file_name (str): The file name.
            expires_in (int): The expiration time for the presigned url.
        """
        return self._create_presigned_request(
            bucket_name=bucket_name,
            action=RequestAction.PUT_OBJECT,
            file_name=file_name,
            expires_in=expires_in,
        )

    def upload_object_to_s3(self, file: any, file_name: str, bucket_name: str):
        """Upload a file to an S3 bucket.

        Args:
            file (any): The file to upload.
            filename (str): The name the file should have in the S3 bucket.
            bucket_name (str): The bucket name.
        """
        with file as request_file:
            self.client.upload_fileobj(
                request_file,
                bucket_name,
                file_name,
            )

    def delete_file(self, file_name: str, bucket_name: str) -> None:
        """
        Deletes a file by name and bucket name.

        Args:
            file_name (str): The file name to be eliminated.
            bucket_name (str): The bucket name.
        """
        self.client.delete_object(
            Bucket=bucket_name,
            Key=file_name,
        )

    def _create_presigned_request(
        self,
        bucket_name: str,
        action: RequestAction,
        file_name: str,
        expires_in: int = 300,
    ):
        """
        Creates a presigned URL for an S3 bucket object.

        Args:
            bucket_name (str): The target bucket name.
            action (RequestAction): The request action.
            file_name (str): The file name.
            expires_in (int): The expiration time for the presigned url.
        """
        method_parameters = {
            RepositoryConstants.BUCKET: bucket_name,
            RepositoryConstants.KEY: file_name,
        }

        return self.client.generate_presigned_url(
            ClientMethod=action.value,
            Params=method_parameters,
            ExpiresIn=expires_in,
        )

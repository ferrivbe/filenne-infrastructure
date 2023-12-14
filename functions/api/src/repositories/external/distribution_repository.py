import base64
import datetime
import json

import boto3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from repositories.environment_repository import EnvironmentRepository


class DistributionRepository:
    """
    Handles all transactions for CloudFront distribution.
    """

    def __init__(self):
        """
        Initializes a new instance of DistributionRepository class.
        """
        environment_repository = EnvironmentRepository()

        self.public_key_id: str = environment_repository.get_cloudfront_public_key_id()
        self.private_key: str = environment_repository.get_cloudfront_private_key()

        self.client = boto3.client("cloudfront")

    def create_signed_url(
        self,
        base_url: str,
        file_name: str,
        expire_seconds: int = 300,
    ):
        """
        Create a signed CloudFront URL for a resource.

        Args:
            base_url (str): The base URL for the resource.
            file_name (str): The name of the file to access.
            expire_seconds (int, optional): The number of seconds the URL will be valid. Default is 300 seconds.

        Returns:
            str: The signed CloudFront URL.
        """
        file_url = f"https://{base_url}/{file_name}"

        expire_epoch_time = (
            datetime.datetime.now() + datetime.timedelta(seconds=expire_seconds)
        ).timestamp()

        policy = self._create_cloudfront_policy(file_url, int(expire_epoch_time))

        signature = self._generate_cloudfront_signature(
            policy.encode("utf-8"),
            self.private_key,
        )

        return (
            f"{file_url}?Policy={self._url_base64_encode(policy.encode('utf-8'))}"
            f"&Signature={self._url_base64_encode(signature)}"
            f"&Key-Pair-Id={self.public_key_id}"
        )

    def _create_cloudfront_policy(self, resource: str, expire_epoch_time: int):
        """
        Create a CloudFront policy for a resource and expiration time.

        Args:
            resource (str): The resource to access.
            expire_epoch_time (int): The epoch time when the URL will expire.

        Returns:
            str: The CloudFront policy as a JSON string.
        """
        policy = {
            "Statement": [
                {
                    "Resource": resource,
                    "Condition": {"DateLessThan": {"AWS:EpochTime": expire_epoch_time}},
                }
            ]
        }
        return json.dumps(policy).replace(" ", "")

    def _generate_cloudfront_signature(self, message: bytes, private_key: bytes):
        """
        Generate a CloudFront signature for a given message.

        Args:
            message (bytes): The message to sign.
            private_key (bytes): The private key used for signing.

        Returns:
            bytes: The CloudFront signature.
        """
        private_key_signer = serialization.load_pem_private_key(
            private_key.encode("utf-8"),
            password=None,
            backend=default_backend(),
        )

        return private_key_signer.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA1(),
        )

    def _url_base64_decode(self, data: bytes):
        """
        URL-safe base64 decode the given data.

        Args:
            data (bytes): The data to decode.

        Returns:
            str: The decoded data.
        """
        return (
            base64.b64encode(data)
            .replace(b"-", b"+")
            .replace(b"_", b"=")
            .replace(b"~", b"/")
            .decode("utf-8")
        )

    def _url_base64_encode(self, data: bytes):
        """
        URL-safe base64 encode the given data.

        Args:
            data (bytes): The data to encode.

        Returns:
            str: The URL-safe base64 encoded data.
        """
        return (
            base64.b64encode(data)
            .replace(b"+", b"-")
            .replace(b"=", b"_")
            .replace(b"/", b"~")
            .decode("utf-8")
        )

import os

from common.constants.environment_variables import EnvironmentVariables
from common.exception.http_error import HTTPInternalServerError


class EnvironmentRepository:
    """
    Handles all interactions with environment variables.
    """

    def __init__(self):
        """
        Initializes a new instance of :class:`EnvironmentRepository` class.
        """
        self.environemnt = os.environ

    def get_cloudfront_private_key(self) -> str:
        """
        Retrieves the CloudFront private key environment variable.
        """
        return self._get_environment_variable(
            EnvironmentVariables.CLOUDFRONT_PRIVATE_KEY
        )

    def get_cloudfront_public_key_id(self) -> str:
        """
        Retrieves the CloudFront public key identifier environment variable.
        """
        return self._get_environment_variable(
            EnvironmentVariables.CLOUDFRONT_PUBLIC_KEY_ID
        )

    def get_files_bucket_name(self):
        """
        Retrieves the files bucket name environment variable.
        """
        return self._get_environment_variable(EnvironmentVariables.FILES_BUCKET_NAME)

    def get_file_service_base_url(self):
        """
        Retrieves the file service base URL environment variable.
        """
        return self._get_environment_variable(
            EnvironmentVariables.FILE_SERVICE_BASE_URL
        )

    def _validate_environment_variable(
        self,
        environment_variable: str,
        environment_variable_name: str,
    ):
        """
        Validates if an environment variable is not None.

        :param str environment_variable: The environment variable to validate.
        :param str environment_variable_name: The name of the environment variable.
        :raises HttpInternalServerError: When the environment variable is None.
        """
        if environment_variable is None:
            raise HTTPInternalServerError(
                "EnvironmentVariableMissing",
                "The environment variable '%(name)s' is missing in current context."
                % {"name": environment_variable_name},
            )

    def _get_environment_variable(self, environment_variable_name: str):
        """
        Retrieves the value of an environment variable.

        :param str environment_variable_name: The name of the environment variable.
        :returns: The value of the environment variable.
        :rtype: str
        :raises HttpInternalServerError: When the environment variable is None.
        """
        environment_variable: str = os.getenv(environment_variable_name).replace(
            r"\n",
            "\n",
        )

        self._validate_environment_variable(
            environment_variable=environment_variable,
            environment_variable_name=environment_variable_name,
        )

        return environment_variable

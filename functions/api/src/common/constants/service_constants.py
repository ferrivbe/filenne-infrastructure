class ServiceConstants:
    """
    A class to store constants used in a service.
    """

    CODE = "code"
    """
    str: The code.
    """

    DYNAMO_DB_CLIENT_NAME = "dynamodb"
    """
    str: The DynamoDB client name.
    """

    EMPTY_STRING = ""
    """
    str: The empty string.
    """

    S3_CLIENT_NAME = "s3"
    """
    str: The boto3 simple storage service client name.
    """

    USERNAME = "username"
    """
    str: The username.
    """

    VALUE_ERROR = "ValueError"
    """
    Error code for a value error.
    """

    WILDCARD = "/"
    """
    str: Wildcard character used in certain contexts.

    This constant represents a wildcard character ("/") that is used in specific contexts within the codebase.
    """

    ZERO_ITEMS = 0
    """
    int: The zero items validation.
    """

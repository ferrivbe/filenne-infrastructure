class ErrorCodes:
    """
    Error codes used in the application.
    """

    ENTITY_NOT_FOUND = "%(entity_type)sNotFound"
    """
    Error code for an entity not found.
    """

    INTERNAL_SERVER_ERROR = "InternalServerError"
    """
    Error code for an internal server error.
    """

    INVALID_CONFIRMATION_CODE = "InvalidConfirmationCode"
    """
    Error code for an invalid confirmation code.
    """

    NOT_VALID_PASSWORD = "NotValidPassword"
    """
    Error code for a not valid password.
    """

    STORAGE_TRANSACTION_FAILED_DEPENDENCY = "StorageTransactionFailedDependency"
    """
    Error code for a storage transaction failed dependency
    """

    UNAUTHORIZED_TO_PERFORM_ACTION = "UnauthorizedToPerformAction"
    """
    Error code for unauthorized to perform action.
    """

    USER_ALREADY_EXISTS = "UserAlreadyExists"
    """
    Error code for the user already exists.
    """

    USER_NOT_CONFIRMED = "UserNotConfirmed"
    """
    Error code for the user not confirmed.
    """

    USER_NOT_FOUND = "UserNotFound"
    """
    Error code for the user not found.
    """

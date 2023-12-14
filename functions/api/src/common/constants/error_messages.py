class ErrorMessages:
    """
    A constant repository containing all error messages.
    """

    ENTITY_NOT_FOUND = "The entity '%(entity_type)s' with id '%(id)s' does not exist for this user in this service."
    """
    The entity not found error message.
    """

    STORAGE_UPLOAD_FAILED_DEPENDENCY = "The upload transaction failed."
    """
    The storage upload failed dependency error message.
    """

    USER_NOT_FOUND_IN_REQUEST = (
        "The user is not able to execute the request, perhaps it does not exist."
    )
    """
    The user was not found in the request error message.
    """

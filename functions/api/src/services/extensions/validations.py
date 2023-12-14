from http import HTTPStatus

from common.constants.error_codes import ErrorCodes
from common.constants.error_messages import ErrorMessages
from common.exception.http_error import HTTPError


class Validations:
    """
    Repository for all entity validations.
    """

    def is_none_or_empty(entity: [], entity_type: str, id: str):
        """
        Raises HTTPError if array is none or empty
        """
        if entity is None or len(entity) == 0:
            raise HTTPError(
                HTTPStatus.NOT_FOUND,
                error_code=ErrorCodes.ENTITY_NOT_FOUND
                % {"entity_type": entity_type.capitalize()},
                message=ErrorMessages.ENTITY_NOT_FOUND
                % {"entity_type": entity_type, "id": id},
            )

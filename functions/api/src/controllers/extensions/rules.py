import re
from http import HTTPStatus

from common.exception.http_error import HTTPError


class Rules:
    """
    Handles all rule checking for controllers.
    """

    def __init__(self):
        """
        Initializes a new instance of Rules class.
        """
        self.file_name_regex = r"^[a-záéíóúñüA-ZÁÉÍÓÚÑÜ0-9_-]+\.[a-zA-Z0-9]+$"

    def match_filename_regex(self, file_name: str) -> None:
        """
        Matches the filename to the regex expression.

        Args:
            file_name (str): The file name to be matched with the regex.
        """
        self._match_regex(
            regex=self.file_name_regex,
            entity=file_name,
            entity_name="FileName",
        )

    def _match_regex(self, regex: str, entity: str, entity_name: str) -> None:
        """
        Matches values to a regex.

        Args:
            regex (str): The regular expression to be compared with.
            entity (str): The string entity to be evaluated.
            entity_name (str): The entity name provided for formatting exceptions.
        """
        if not re.match(regex, entity, re.UNICODE):
            raise HTTPError(
                HTTPStatus.BAD_REQUEST,
                "%(entity_name)sInvalid" % {"entity_name": entity_name},
                "The %(entity_name)s with value '%(value)s' does not match the regular expression '%(regex)s'."
                % {
                    "entity_name": entity_name,
                    "value": entity,
                    "regex": regex,
                },
            )

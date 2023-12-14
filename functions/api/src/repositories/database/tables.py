from enum import Enum


class Table(Enum):
    """
    Contains all table definitions.
    """

    def __str__(self):
        """
        Returns the string format of the enum member value.
        """
        return str(self.value)

    file = "file"
    """
    The file table in dynamodb context.
    """

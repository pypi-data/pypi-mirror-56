from typing import Union

from datalogue.errors import DtlError, _enum_parse_error
from datalogue.utils import SerializableStringEnum


class Permission(SerializableStringEnum):
    """
    Class that handles all permission types
    """
    Share = "Share"
    Write = "Write"
    Read = "Read"

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error("permission type", s))

    @staticmethod
    def from_string(string: str) -> Union[DtlError, 'Permission']:
        return SerializableStringEnum.from_str(Permission)(string)


# TODO change to the standard Permission Model (write, read, share)
class OntologyPermission(SerializableStringEnum):
    """
    Class that handles Ontology permission types
    """
    Write = "Write"
    Read = "Read"

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error("Ontology permission type", s))

    @staticmethod
    def from_string(string: str) -> Union[DtlError, 'OntologyPermission']:
        return SerializableStringEnum.from_str(OntologyPermission)(string)


# TODO change to the standard Permission Model (write, read, share)
class CredentialPermission(SerializableStringEnum):
    """
    Class that handles Credential permission types
    """
    Write = "Write"
    Use = "Use"
    Read = "Read"

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error("permission type", s))

    @staticmethod
    def from_string(string: str) -> Union[DtlError, 'CredentialPermission']:
        return SerializableStringEnum.from_str(CredentialPermission)(string)

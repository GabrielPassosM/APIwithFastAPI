import re

from libs.base_types.pydantic import PydanticConversor


class EmailAddress(str, PydanticConversor):
    class _InvalidEmail(Exception):
        pass

    def __new__(cls, address: str):
        if not cls._is_valid_email(address):
            raise cls._InvalidEmail(f"Invalid email address: {address}")
        return str.__new__(cls, address.lower())

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

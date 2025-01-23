from libs.base_types.pydantic import PydanticConversor


class Password(str, PydanticConversor):
    class _InvalidPassword(Exception):
        pass

    def __new__(cls, password: str):
        if not cls._is_valid_password(password):
            raise cls._InvalidPassword(f"Invalid password length (3 - 50): {password}")
        return str.__new__(cls, password)

    @staticmethod
    def _is_valid_password(password: str) -> bool:
        return 3 <= len(password) <= 50

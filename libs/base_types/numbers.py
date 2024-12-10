from libs.base_types.pydantic import PydanticConversor


class PositiveNumber(int, PydanticConversor):
    class _InvalidNumber(Exception):
        pass

    def __init__(self, valor):
        if valor < 0:
            raise self._InvalidNumber("Number must be positive")

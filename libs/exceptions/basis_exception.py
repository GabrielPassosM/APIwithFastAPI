from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class BasisException(HTTPException):
    detail: str
    status_code: int

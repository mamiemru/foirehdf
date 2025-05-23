from dataclasses import dataclass
from typing import Optional, Any

from backend.dto.response_dto import ResponseDto


@dataclass
class Meta:
    timestamp: str
    requestId: str

@dataclass
class SuccessResponse(ResponseDto):
    message: str
    data: Any
    meta: Optional[Meta] = None

    def __init__(self, data, message="", status=200):
        self.message = message
        self.status = status
        self.data = data

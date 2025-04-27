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

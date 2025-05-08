from dataclasses import dataclass
from typing import Optional, Dict

from backend.dto.response_dto import ResponseDto


@dataclass
class ErrorResponse(ResponseDto):
    message: str
    errors: Optional[Dict[str, str]] = None
    
    def __init__(self, data, message="", status=500):
        self.message = message
        self.status = status
        self.data = data

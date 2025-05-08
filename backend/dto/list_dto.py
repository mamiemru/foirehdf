from dataclasses import dataclass
from typing import List

from backend.dto.response_dto import ResponseDto

@dataclass
class ListResponse(ResponseDto):
    data: List

    def __init__(self, data, message="", status=200):
        self.message = message
        self.status = status
        self.data = data

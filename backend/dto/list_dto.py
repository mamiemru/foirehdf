from dataclasses import dataclass
from typing import List

from backend.dto.response_dto import ResponseDto

@dataclass
class ListResponse(ResponseDto):
    data: List

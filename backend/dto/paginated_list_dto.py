from dataclasses import dataclass
from typing import List

from backend.dto.response_dto import ResponseDto

@dataclass
class Pagination:
    page: int
    perPage: int
    totalPages: int
    totalItems: int

@dataclass
class PaginatedResponse(ResponseDto):
    data: List
    pagination: Pagination

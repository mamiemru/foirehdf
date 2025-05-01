from typing import List
from typing import Dict

from pydantic import ValidationError

from backend.services.attractionService import list_attractions
from backend.services.attractionService import list_attractions_names_and_id
from backend.services.attractionService import list_attraction_images_to_dto
from backend.services.attractionService import get_attraction_by_id
from backend.services.attractionService import list_attractions_names
from backend.services.attractionService import create_attraction
from backend.services.attractionService import update_attraction
from backend.models.attractionModel import Attraction

from backend.dto.attraction_dto import AttractionDTO, AttractionImageDTO
from backend.dto.paginated_list_dto import PaginatedResponse, Pagination
from backend.dto.response_dto import ResponseDto
from backend.dto.error_dto import ErrorResponse
from backend.dto.success_dto import SuccessResponse
from backend.dto.list_dto import ListResponse


def list_attractions_endpoint() -> ResponseDto:

    try:
        rides: List[AttractionDTO] = list_attractions()
        rides_count: int = len(rides)
    except Exception as e:
        return ErrorResponse(
            status=500,
            message=str(e),
            errors={e.name: str(e)}
        )
    else:
        return PaginatedResponse(
            status=200,
            data=rides,
            pagination=Pagination(page=1, perPage=rides_count, totalPages=1, totalItems=rides_count)
        )

def create_attraction_endpoint(attraction_dict: Dict, attraction_image=None) -> ResponseDto:
    try:
        ride_dto: AttractionDTO = create_attraction(attraction_dict, attraction_image)
    except KeyError as e:
        return ErrorResponse(
            status=400,
            message=str(e)
        )
    except ValidationError as e:
        return ErrorResponse(
            status=400,
            message="One of your information is wrong or empty, check your form below",
            errors={err['loc'][0]: err['msg'] for err in e.errors()}
        )
    except Exception as e:
        return ErrorResponse(
            status=500,
            message=str("An error occurred when creating the new attraction"),
            errors={e.name: str(e)}
        )
    else:
        return SuccessResponse(
            status=201,
            message=f"The attraction {ride_dto.name} has been created",
            data=ride_dto
        )

def update_attraction_endpoint(attraction_dict: Dict, id: str) -> ResponseDto:
    try:
        ride_dto: AttractionDTO = update_attraction(id, attraction_dict)
    except KeyError as e:
        return ErrorResponse(
            status=400,
            message=str(e)
        )
    except ValidationError as e:
        return ErrorResponse(
            status=400,
            message="One of your information is wrong or empty, check your form below",
            errors={err['loc'][0]: err['msg'] for err in e.errors()}
        )
    except Exception as e:
        return ErrorResponse(
            status=500,
            message=str("An error occurred when updating the new attraction"),
            errors={e.name: str(e)}
        )
    else:
        return SuccessResponse(
            status=201,
            message=f"The attraction {ride_dto.name} has been updated",
            data=ride_dto
        )

def list_attractions_names_endpoint() -> ResponseDto:
    rides_names: List[str] = list_attractions_names()
    return ListResponse(
        status=200,
        data=rides_names
    )

def list_attractions_names_and_id_endpoint() -> ResponseDto:
    rides_names: Dict[str, List[str]] = list_attractions_names_and_id()
    return SuccessResponse(
        status=200,
        message="",
        data=rides_names
    )


def get_attraction_image_by_id_endpoint(attraction_id: str) -> ResponseDto:
    attraction_images: List[AttractionImageDTO] = list_attraction_images_to_dto(attraction_id)
    return SuccessResponse(
        status=200,
        message="",
        data=attraction_images[0] if attraction_images else None
    )


def get_attraction_by_id_endpoint(attraction_id: str) -> ResponseDto:
    attraction: AttractionDTO = get_attraction_by_id(attraction_id)
    if attraction:
        return SuccessResponse(
            status=200,
            message="",
            data=attraction
        )
    return ErrorResponse(
        status=404,
        message="Attraction not found"
    )

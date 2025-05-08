
from typing import Dict

from pydantic import ValidationError
from backend.dto.error_dto import ErrorResponse
from backend.dto.list_dto import ListResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse
from backend.models.locationModel import LocationDTO
from backend.services.locationService import list_locations
from backend.services.locationService import create_location
from backend.services.locationService import update_location


def create_location_endpoint(location_dict: Dict) -> ResponseDto:
    try:
        location_dto: LocationDTO = create_location(location_dict=location_dict)
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
            message=str("An error occurred when creatting the new location"),
            errors={e.name: str(e)}
        )
    else:
        return SuccessResponse(
            status=201,
            message=f"The location has been created",
            data=location_dto
        )


def update_location_endpoint(location_id: str, updated_location_dict: Dict) -> ResponseDto:
    try:
        location_dto = update_location(location_id=location_id, updated_location_dict=updated_location_dict)
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
            message=str("An error occurred when update the new location"),
            errors={'err': str(e)}
        )
    else:
        return SuccessResponse(
            status=201,
            message=f"The location has been updated",
            data=location_dto
        )


def list_locations_endpoint() -> ResponseDto:
    return ListResponse(
        status=200,
        data=list_locations()
    )

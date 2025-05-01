from typing import List
from typing import Dict

from pydantic import ValidationError

from backend.services.manufacturerService import list_manufacturers, delete_manufacturer
from backend.services.manufacturerService import list_manufacturers_names
from backend.services.manufacturerService import create_manufacturer
from backend.services.manufacturerService import validate_manufacturer

from backend.models.manufacturerModel import Manufacturer

from backend.dto.manufacturer_dto import ManufacturerDto
from backend.dto.response_dto import ResponseDto
from backend.dto.error_dto import ErrorResponse
from backend.dto.success_dto import SuccessResponse
from backend.dto.list_dto import ListResponse


def list_manufacturer_endpoint() -> ResponseDto:

    try:
        manufacturers: List[ManufacturerDto] = list_manufacturers()
    except Exception as e:
        return ErrorResponse(
            status=500,
            message=str(e),
            errors={e.name: str(e)}
        )
    else:
        return ListResponse(
            status=200,
            data=manufacturers
        )

def create_manufacturer_endpoint(manufacturer_dict: Dict) -> ResponseDto:

    try:
        manufacturer: Manufacturer = validate_manufacturer(manufacturer_dict)
        manufacturer_dto: ManufacturerDto = create_manufacturer(manufacturer)
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
            message=str("An error occurred when adding the manufacturer"),
            errors={e.name: str(e)}
        )
    else:
        return SuccessResponse(
            status=201,
            message=f"Manufacturer {manufacturer.name} has been added",
            data=manufacturer_dto
        )

def list_manufacturer_names_endpoint() -> ResponseDto:
    manufacturer_names: List[str] = list_manufacturers_names()
    return ListResponse(
        status=200,
        data=manufacturer_names
    )

def delete_manufacturer_endpoint(manufacturer_id: str) -> ResponseDto:
    try:
        delete_manufacturer(manufacturer_id)
    except Exception as e:
        return ErrorResponse(
            status=500,
            message=str("An error occurred when adding the manufacturer"),
            errors={e.name: str(e)}
        )
    else:
        return SuccessResponse(
            status=404,
            message=f"Manufacturer has been deleted",
            data=None
        )

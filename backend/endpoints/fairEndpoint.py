
import datetime
from typing import Dict, List

import pandas
from pydantic_core._pydantic_core import ValidationError

from backend.dto.error_dto import ErrorResponse
from backend.dto.list_dto import ListResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.models.fairModel import FairBaseDTO, FairDTO, FairStatus


from backend.services.fairService import create_fair, create_hidden_fair, get_fair_detailed, get_fair, list_fair_months
from backend.services.fairService import delete_fair, list_fair_locations
from backend.services.fairService import list_fairs_containing_ride_id, update_fair
from backend.services.fairService import list_fairs


def create_fair_endpoint(fair_dict: Dict, hidden_fair: bool = False) -> ResponseDto:
    try:
        if hidden_fair:
            fair_dto: FairBaseDTO = create_hidden_fair(fair_dict)
        else:
            fair_dto: FairDTO = create_fair(fair_dict)
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
            message=f"The attraction {fair_dto.name} has been created",
            data=fair_dto
        )
        
def update_fair_endpoint(id: str, updated_fair_dict: Dict) -> ResponseDto:
    try:
        fair_dto = update_fair(id=id, updated_fair_dict=updated_fair_dict)
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
            errors={'err': str(e)}
        )
    else:
        return SuccessResponse(
            status=201,
            message=f"The attraction {fair_dto.name} has been updated",
            data=fair_dto
        )


def list_fairs_endpoint() -> ResponseDto:
    return ListResponse(data=list_fairs())

def list_fair_sort_by_status_endpoint(search_fair_query: Dict=None) -> ResponseDto:
    fairs: List[FairDTO] = list_fairs(search_fair_query=search_fair_query)
    pd_dict: List[Dict[str, str]] = list()
    response: Dict = {
        'fairs': {
            str(FairStatus.INCOMING): [],
            str(FairStatus.DONE): [],
            str(FairStatus.CURRENTLY_AVAILABLE): []
        },
        'map': [],
        'gantt': None
    }

    for fair in fairs:
        response['fairs'][fair.fair_status].append(fair)
        
        if fair.location.lng and fair.location.lat:
            color = '#33cc33' if fair.fair_available_today else '#ff9900' if fair.fair_incoming else '#0066cc'
            size = 7 if fair.fair_available_today else 5 if fair.fair_incoming else 2
            response['map'].append(
                {'color': color, 'lng': fair.location.lng, 'lat': fair.location.lat, 'size': size}
            )
            
        pd_dict.append({
            "task": fair.location.city,
            "start": fair.start_date,
            "finish": fair.end_date,
            "resource": fair.location.city,
            "color": '#33cc33' if fair.fair_available_today else '#ff9900' if fair.fair_incoming else '#0066cc',
            "date": fair.days_before_start_date if fair.fair_incoming else fair.days_before_end_date if fair.fair_available_today else "Fair Done",
            "start_date": fair.start_date.strftime('%d %B %Y'),
            "end_date": fair.end_date.strftime('%d %B %Y'),
            "name": fair.name
        })
    
    for key, fair_list in response['fairs'].items():
        response['fairs'][key] = sorted(fair_list, key=lambda fair: fair.start_date, reverse=True)


    response['gantt'] = pandas.DataFrame(pd_dict)
    return SuccessResponse(data=response)


def get_fair_endpoint(id: str) -> ResponseDto:
    fair = get_fair(id)
    if fair:
        return SuccessResponse(data=fair)
    return ErrorResponse(status=404, message="Fair not found")

def get_fair_detailed_endpoint(id: str) -> ResponseDto:
    fair = get_fair_detailed(id)
    if fair:
        return SuccessResponse(data=fair)
    return ErrorResponse(status=404, message="Fair not found")


def delete_fair_endpoint(fair_id: str) -> ResponseDto:
    try:
        delete_fair(fair_id)
    except Exception as e:
        return ErrorResponse(status=500, message=str("An error occurred when adding the fair"), errors={e.name: str(e)})
    else:
        return SuccessResponse(status=404, message=f"Fair has been deleted", data=None)

def list_fairs_containing_ride_id_endpoint(ride_id: str) -> ResponseDto:
    return SuccessResponse(data=list_fairs_containing_ride_id(ride_id))

def list_fair_locations_endpoint() -> ResponseDto:
    return ListResponse(data=list_fair_locations())

def list_fair_months_endpoint() -> ResponseDto:
    return ListResponse(data=list_fair_months())

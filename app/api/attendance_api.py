from fastapi import APIRouter, HTTPException, Depends
from app.models.attendance_model import AttendanceModel, LateReason, LeaveReason
from app.services import attendance_services as service
from app.api.authentication import authenticate_user

attendance_router = APIRouter()

#___________________________________________________________________________________________________________________

#Create a New Attendance Record API
@attendance_router.post("/attendance-record/{user_id}")
async def create_attendance_record_endpoint(user_id: str, user_auth: bool = Depends(authenticate_user)):

    try:
        
        if not user_auth:
            raise HTTPException(status_code = 401, detail = "Unauthorized User")
        
        created_record = await service.create_attendance_record(user_id)
        return created_record

    except ValueError as error:
        raise HTTPException(status_code = 404, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________
    
#Check In For Attendance API
@attendance_router.post("/check-in/{user_id}")
async def check_in_endpoint(user_id: str , reason: LateReason, user_auth: bool = Depends(authenticate_user)):

    try:

        if not user_auth:
            raise HTTPException(status_code = 401, detail = "Unauthorized User")
        
        check_in = await service.check_in_service(user_id , reason.model_dump())
        return check_in

    except ValueError as error:
        raise HTTPException(status_code = 404, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________
    
#Check Out For Attendance API
@attendance_router.post("/check-out/{user_id}")
async def check_out_endpoint(user_id: str , reason: LeaveReason, user_auth: bool = Depends(authenticate_user)):

    try:

        if not user_auth:
            raise HTTPException(status_code = 401, detail = "Unauthorized User")
        
        check_out = await service.check_out_service(user_id , reason.model_dump())
        return check_out

    except ValueError as error:
        raise HTTPException(status_code = 404, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________
    
#Get All User Attendance Records API
@attendance_router.get("/attendance-records/{user_id}")
async def get_all_user_attendance_records_endpoint(user_id: str,  user_auth: bool = Depends(authenticate_user)):

    try:

        if not user_auth:
            raise HTTPException(status_code = 401, detail = "Unauthorized User")
        
        all_records = await service.get_all_user_attendance_records(user_id)
        return all_records

    except ValueError as error:
        raise HTTPException(status_code = 404, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________
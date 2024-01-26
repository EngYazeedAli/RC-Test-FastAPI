from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator
from dateutil import parser

class AttendanceModel(BaseModel):

    attendance_date: Optional[datetime] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    checked_in: bool = False
    checked_out: bool = False
    late_mark: bool = False
    leave_mark: bool = False
    late_reason: Optional[str] = None
    lave_reason: Optional[str] = None 
    attended_hours: float = 0.0
    user_id: str

    @validator("attendance_date", pre = True, always = True)
    def set_date_to_now(cls, value):
        value = parser.isoparse(datetime.today().strftime("%Y-%m-%d") + "T00:00:00.000Z")
        return value 
    
    @validator("check_in", pre = True, always = True)
    def set_check_in_to_none(cls, value):
        value = None;
        return value 
    
    @validator("check_out", pre = True, always = True)
    def set_check_out_to_none(cls, value):
        value = None;
        return value
    
    @validator("attended_hours", pre = True, always = True)
    def round_attended_hours(cls, value):
        return round(value, 1)

class LateReason(BaseModel):
    late_reason: Optional[str] = None

class LeaveReason(BaseModel):
    leave_reason: Optional[str] = None

    
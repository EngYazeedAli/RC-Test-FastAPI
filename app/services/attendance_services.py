from bson import ObjectId
from datetime import datetime, time
from app.config.db import attendance_collection as collection
from dateutil import parser
import pytz

sa_timezone = pytz.timezone('Asia/Riyadh')
#___________________________________________________________________________________________________________________

#Create a New Attendance Record Service
async def create_attendance_record(user_id):

    try:
        
        attendance_date = parser.isoparse(datetime.now(sa_timezone).strftime("%Y-%m-%d"))

        existed_attendance_record = collection.find_one({"user_id": user_id, "attendance_date": attendance_date})

        if existed_attendance_record:
            existed_attendance_record["_id"] = str(existed_attendance_record["_id"])
            return ({"existed_record": True, "attendance_record": existed_attendance_record})

        attendance_record = {
            "attendance_date": attendance_date,
            "check_in": None,
            "check_out": None,
            "checked_in": False,
            "checked_out": False,
            "late_mark": False,
            "leave_mark": False,
            "late_reason": None,
            "lave_reason": None, 
            "attended_hours": 0.0,
            "user_id": user_id
        }

        collection.insert_one(attendance_record)
        attendance_record["_id"] = str(attendance_record["_id"])
        return ({"existed_record": False, "attendance_record": attendance_record})

    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
#Check In For Attendance Service
async def check_in_service(user_id, reason):

    try:
        attendance_date = parser.isoparse(datetime.now(sa_timezone).strftime("%Y-%m-%d"))
        attendance_record =  collection.find_one({"user_id": user_id, "attendance_date": attendance_date})

        if not attendance_record:
            raise ValueError("No Attendance Record Found")
        
        if attendance_record["checked_in"] is True:
            raise ValueError("Already Checked In")



    #_______________________________________________________________________________

        #For testing purposes

        #test_time = datetime(year = 2024, month = 1, day = 26, hour = 7, minute = 25)
        #now = test_time

    #_______________________________________________________________________________
        
        now = datetime.now(sa_timezone).time()
        late_check_in = (now >= time(8, 30, 0) and now < time(16, 0, 0))
        normal_check_in = (now >= time(7, 0, 0) and now <= time(8, 29, 59))

        if late_check_in:
            attendance_record["check_in"] = attendance_date.replace(hour = now.hour, minute = now.minute)
            attendance_record["checked_in"] = True
            attendance_record["late_mark"] = True
            attendance_record["late_reason"] = reason["late_reason"]

        elif normal_check_in:
            attendance_record["check_in"] = attendance_date.replace(hour = now.hour, minute = now.minute)
            attendance_record["checked_in"] = True

        else:
            raise ValueError("Attendance Time is Over")

        collection.update_one(
            {"_id": ObjectId(attendance_record["_id"])},
            {"$set": attendance_record}
        )

        attendance_record["_id"] = str(attendance_record["_id"])
        return attendance_record
 
    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
#Check out for attendance service
async def check_out_service(user_id, reason):

    try:
        attendance_date = parser.isoparse(datetime.now(sa_timezone).strftime("%Y-%m-%d"))
        attendance_record =  collection.find_one({"user_id": user_id, "attendance_date": attendance_date})

        if not attendance_record:
            raise ValueError("No Attendance Record Found")
        
        if attendance_record["checked_out"] is True:
            raise ValueError("Already Checked Out")
        
        if attendance_record["checked_in"] is False:
            raise ValueError("Please Check In First")
        

    #_______________________________________________________________________________

        #For testing purposes

        #test_time = datetime(year = 2024, month = 1, day = 26, hour = 15, minute = 5)
        #now = test_time
        
    #_______________________________________________________________________________


        now = datetime.now(sa_timezone).time()
        early_check_out = (now >= time(7, 0, 1) and now < time(15, 0, 0))
        normal_check_out = (now >= time(15, 0, 1) and now < time(16, 5, 0))

        # Calculate attended hours
        now_duration = datetime.now(sa_timezone)
        check_in_time = attendance_record["check_in"].astimezone(sa_timezone)
        attended_hours = (now_duration - check_in_time).total_seconds() / 3600

        if early_check_out:
            attendance_record["check_out"] = attendance_date.replace(hour = now.hour, minute = now.minute)
            attendance_record["checked_out"] = True
            attendance_record["leave_mark"] = True
            attendance_record["leave_reason"] = reason["leave_reason"]
            attendance_record["attended_hours"] = round(attended_hours, 1)

        elif normal_check_out:
            attendance_record["check_out"] = attendance_date.replace(hour = now.hour, minute = now.minute)
            attendance_record["checked_out"] = True
            attendance_record["attended_hours"] = round(attended_hours, 1)

        else:
            raise ValueError("Attendance Time is Over")

        collection.update_one(
            {"_id": ObjectId(attendance_record["_id"])},
            {"$set": attendance_record}
        )

        attendance_record["_id"] = str(attendance_record["_id"])
        return attendance_record
 
    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
#Get All User Attendance Records Service
async def get_all_user_attendance_records(user_id):

    try:

        all_records = []
        existed_records = collection.find({"user_id": user_id})

        for attendance in existed_records:
            attendance["_id"] = str(attendance["_id"])
            all_records.append(attendance)

        if not all_records:
            raise ValueError("No Attendance Records Found")

        return all_records
        
    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
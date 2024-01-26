from bson import ObjectId
from datetime import datetime
from app.config.db import attendance_collection as collection
from dateutil import parser

#___________________________________________________________________________________________________________________

#Create a New Attendance Record Service
async def create_attendance_record(user_id , attendance):

    try:

        attendance_date = parser.isoparse(datetime.today().strftime("%Y-%m-%d"))

        existed_attendance_record = collection.find_one({"user_id": user_id, "attendance_date": attendance_date})

        if existed_attendance_record:
            return ({"existed_record": True, "attendance_record": attendance})

        attendance_data = {
            **attendance,
            "user_id": user_id
        }

        collection.insert_one(attendance_data)
        return ({"existed_record": False, "attendance_record": attendance})


    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
#Check In For Attendance Service
async def check_in_service(user_id, reason):

    try:
        attendance_date = parser.isoparse(datetime.today().strftime("%Y-%m-%d"))
        attendance_record =  collection.find_one({"user_id": user_id, "attendance_date": attendance_date})

        if not attendance_record:
            raise ValueError("No Attendance Record Found")
        
        if attendance_record["checked_in"] is True:
            raise ValueError("Already Checked In")



    #_______________________________________________________________________________

        #For testing purposes

        test_time = datetime(year = 2024, month = 1, day = 26, hour = 7, minute = 25)
        now = test_time

    #_______________________________________________________________________________
        
        #now = datetime.utcnow()
        late_check_in = (now.hour >= 8 and now.minute >= 30) and (now.hour < 16)
        normal_check_in = (now.hour == 7 and now.minute >= 0 and now.second >= 0) or (now.hour == 8 and now.minute <= 29 and now.second <= 59)

        print(normal_check_in)

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
        attendance_date = parser.isoparse(datetime.today().strftime("%Y-%m-%d"))
        attendance_record =  collection.find_one({"user_id": user_id, "attendance_date": attendance_date})

        if not attendance_record:
            raise ValueError("No Attendance Record Found")
        
        if attendance_record["checked_out"] is True:
            raise ValueError("Already Checked Out")
        
        if attendance_record["checked_in"] is False:
            raise ValueError("Please Check In First")
        

    #_______________________________________________________________________________

        #For testing purposes

        test_time = datetime(year = 2024, month = 1, day = 26, hour = 15, minute = 5)
        now = test_time
        
    #_______________________________________________________________________________


        #now = datetime.utcnow()
        early_check_out = (now.hour >= 7 and now.hour < 15)
        normal_check_out = (now.hour >= 15 and now.hour <= 16 and now.minute <= 5)

        # Calculate attended hours
        check_in_time = attendance_record["check_in"]
        attended_hours = (now - check_in_time).total_seconds() / 3600

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
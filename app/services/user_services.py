from bson import ObjectId
import bcrypt
import jwt
from app.config.db import user_collection as collection

#___________________________________________________________________________________________________________________

#Create a New User Service
async def create_user_service(user_data):

    try:

        existed_user = collection.find_one({"email": user_data["email"]})

        if existed_user:
            raise ValueError("User Already Exists")


        created_user = collection.insert_one(user_data)

        if created_user:
            existed_user = collection.find_one({"_id": created_user.inserted_id})

        existed_user["_id"] = str(existed_user["_id"])
        return existed_user

    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
#Get a User by ID Service
async def get_user_service(user_id):

    try:

        object_id = ObjectId(user_id)

        existed_user = collection.find_one({"_id": object_id})

        if existed_user["deleted"] is True:
            raise ValueError("User is Deleted")

        if existed_user:
            existed_user["_id"] = str(existed_user["_id"])
            return existed_user
        
        else:
            raise ValueError("User Not Found")
        
    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
#Get All Users Service
async def get_users_service():

    try:

        all_users = []
        existed_users = collection.find({{"role": "user", "delete": False}})

        for user in existed_users:
            user["_id"] = str(user["_id"])
            all_users.append(user)
        
        if not all_users:
            raise ValueError("No Users Found")

        return all_users
    
    except Exception as error:
        raise ValueError(str(error))   
#___________________________________________________________________________________________________________________
    
#Update User by ID Service
async def update_user_service(user_data, user_id):

    try:

        object_id = ObjectId(user_id)

        existed_user = collection.find_one({"_id": object_id})

        if not existed_user:
            raise ValueError("User Not Found")

        if existed_user["deleted"] is True:
            raise ValueError("User is Deleted")

        if user_data["first_name"]:
            existed_user["first_name"] = user_data["first_name"]

        if user_data["last_name"]:
            existed_user["last_name"] = user_data["last_name"]

        if user_data["email"]:
            existed_user["email"] = user_data["email"]

        if user_data["password"]:
            existed_user["password"] = user_data["password"]

        collection.update_one({"_id": object_id}, {"$set": existed_user})
        
        existed_user["_id"] = str(existed_user["_id"])
        return existed_user
        
    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
   
#Delete a user by ID Service (Mark as Deleted)
async def delete_user_service(user_id):

    try:
       
        object_id = ObjectId(user_id)

        existed_user = collection.find_one({"_id": object_id})

        if not existed_user:
            raise ValueError("User Not Found")


        if existed_user["deleted"] is True:
            raise ValueError("User is Already Deleted")

        if existed_user:
            deleted_user = collection.update_one({"_id": object_id}, {"$set": {"deleted": True}})
            
            if deleted_user.modified_count > 0:
                return ("User is Deleted Successfully")
            
            else:
                raise ValueError("User is Not Deleted")
        
        else:
            raise ValueError("User Not Found")
    
    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________

#Login Service
async def login(user):

    try:
        email = user["email"].lower()
        password = user["password"]

        existed_user = collection.find_one({"email": email})

        if not existed_user:
            raise ValueError("User Not Found")

        if existed_user["deleted"] is True:
            raise ValueError("User is Deleted")

        password_match = bcrypt.checkpw(password.encode('utf-8'), existed_user["password"].encode('utf-8'))

        if not password_match:
            raise ValueError("Password is Incorrect")
        
        user_id = str(existed_user["_id"])
        role = existed_user["role"]

        # Generate JWT Token
        token_payload = {"user_id": user_id, "role": role}
        token = jwt.encode(token_payload, "Royal_Secret_&@0548", algorithm = "HS256")

        existed_user["_id"] = str(existed_user["_id"])

        return {
            "user_info": existed_user, 
            "role": role, 
            "token": token
        }

    except Exception as error:
        raise ValueError(str(error))
#___________________________________________________________________________________________________________________
    
async def create_admin_user():

    existed_admin = collection.find_one({"email": "admin@system.com"})

    if not existed_admin:

        admin_data = {
            "first_name": "System",
            "last_name": "Admin",
            "email": "admin@system.com",
            "password": bcrypt.hashpw("admin@0548".encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8'),
            "role": "admin",
            "deleted": False
        }

        collection.insert_one(admin_data)
        print ("Admin User Created")
#___________________________________________________________________________________________________________________
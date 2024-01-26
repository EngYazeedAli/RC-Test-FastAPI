from fastapi import APIRouter, HTTPException, Depends, Body
from app.models.user_model import UserModel, UserLogin, TokenModel
from app.services import user_services as service
from app.api.authentication import authenticate_user, validate_token

user_router = APIRouter()

#___________________________________________________________________________________________________________________

#Create a New User API
@user_router.post("/user")
async def create_user_endpoint(user: UserModel, admin_auth: dict = Depends(authenticate_user)):

    try:

        if admin_auth["role"] != "admin":
            raise HTTPException(status_code = 401, detail = "Unauthorized")
        
        created_user = await service.create_user_service(user.model_dump())
        return created_user

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________

#Get a User by ID API (For Admin Only)
@user_router.get("/user/{user_id}")
async def get_user_endpoint(user_id: str, admin_auth: dict = Depends(authenticate_user)):

    try:

        if admin_auth["role"] != "admin":
            raise HTTPException(status_code = 401, detail = "Unauthorized")
        
        existed_user = await service.get_user_service(user_id)
        return  existed_user

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________
    
#Get a User by ID API (For User Only)
@user_router.get("/my_info/{user_id}")
async def get_user_endpoint(user_id: str, user_auth: dict = Depends(authenticate_user)):

    try:

        if user_auth["role"] != "user":
            raise HTTPException(status_code = 401, detail = "User Unauthorized")
        
        existed_user = await service.get_user_service(user_id)
        return  existed_user

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________

#Get All Users API
@user_router.get("/users")
async def get_all_user_endpoint(admin_auth: dict = Depends(authenticate_user)):

    try:

        if admin_auth["role"] != "admin":
            raise HTTPException(status_code = 401, detail = "Unauthorized")
        
        all_users = await service.get_users_service()
        return all_users

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________

#Update a User by ID API
@user_router.put("/user/{user_id}")
async def update_user_endpoint(user: UserModel , user_id: str, admin_auth: dict = Depends(authenticate_user)):

    try:

        if admin_auth["role"] != "admin":
            raise HTTPException(status_code = 401, detail = "Unauthorized")
        
        updated_user = await service.update_user_service(user.model_dump(), user_id)
        return updated_user

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________

#Delete a User by ID API (Mark as Deleted)
@user_router.delete("/user/{user_id}")
async def delete_user_endpoint(user_id: str, admin_auth: dict = Depends(authenticate_user)):

    try:

        if admin_auth["role"] != "admin":
            raise HTTPException(status_code = 401, detail = "Unauthorized")
        
        deleted_user = await service.delete_user_service(user_id)
        return deleted_user

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________

#Login API
@user_router.post("/login")
async def login_endpoint(user: UserLogin):

    try:
        existed_user = await service.login(user.model_dump())
        return existed_user

    except ValueError as error:
        raise HTTPException(status_code = 400, detail = str(error))

    except Exception as error:
        raise HTTPException(status_code = 500, detail = str(error))
#___________________________________________________________________________________________________________________
    
#Validate Token API
@user_router.post("/validate-token")
async def validate_token_endpoint(token: TokenModel):


    token_auth = validate_token(token.model_dump()["token"])
    return ({"role": token_auth["role"], "user_id": token_auth["user_id"]})
#___________________________________________________________________________________________________________________
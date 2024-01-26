from fastapi import FastAPI
from app.api.user_api import user_router
from app.api.attendance_api import attendance_router
from app.services.user_services import create_admin_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#______________________________________________________________________________
#CORS Middleware
origins = [
    
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
#______________________________________________________________________________

#Root Route
@app.get('/')
def read_root():
    return "This is The Royal Test FAST API Project. You can find the API Documentation at /docs"

#Create Admin User in The Database on Startup
app.add_event_handler("startup", create_admin_user)
#______________________________________________________________________________

app.include_router(user_router)
app.include_router(attendance_router)
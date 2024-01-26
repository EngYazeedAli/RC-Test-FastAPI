from fastapi import FastAPI
from app.api.user_api import user_router
from app.api.attendance_api import attendance_router
from app.services.user_services import create_admin_user

app = FastAPI()

#______________________________________________________________________________

@app.get('/')
def read_root():
    return "This is The Royal Test FAST API Project. You can find the API Documentation at /docs"

#Create Admin User in The Database on Startup
app.add_event_handler("startup", create_admin_user)
#______________________________________________________________________________

app.include_router(user_router)
app.include_router(attendance_router)
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import ValidationError

security = HTTPBearer()
#___________________________________________________________________________________________________________________________________

#Authentication User Service
def authenticate_user(token: HTTPAuthorizationCredentials = Security(security)):
    
    try:

        payload = jwt.decode(token.credentials, "Royal_Secret_&@0548", algorithms = ["HS256"])

        user_id = payload.get("user_id")
        role = payload.get("role") 

        if user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Authentication Credentials")
        
        return {"user_id":user_id, "role":role}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token Expired")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Authentication Credentials")
#___________________________________________________________________________________________________________________________________
    
#Validate Token Service (For Manual Authentication)
def validate_token(token):
    
    try:

        payload = jwt.decode(token, "Royal_Secret_&@0548", algorithms = ["HS256"])

        user_id = payload.get("user_id")
        role = payload.get("role") 

        if user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Authentication Credentials")
        
        return {"user_id":user_id, "role":role}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token Expired")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Authentication Credentials")
#___________________________________________________________________________________________________________________________________
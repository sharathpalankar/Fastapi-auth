from typing import Any, List
from auth import verify_token
from db import database
from fastapi import Depends, Request,HTTPException,status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from exceptions.request_errors import UserAlreadyExists,RefreshTokenExpired, InvalidCredentials
def get_collection():
    return database['users'] 

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        print(token,"token in bearer to check")

        token_data = verify_token(token)

        #print(token_data,"token data of user")
        self.verify_token_data(token_data)
        
        # if token_data['refresh']:
        #     raise HTTPException(status_code=403, detail="Access token required")
        
        return token_data


    def token_valid(self, token: str) -> bool:
        token_data = verify_token(token)

        return token_data is not None
    
    def verify_token_data(self, token):
        raise NotImplementedError("Please Override this method in child classes")

    

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Access token required, please provide a valid access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
             raise HTTPException(status_code=403, detail="please provide a valid refresh token")

async def get_current_user(token: str = Depends(AccessTokenBearer()), collection=Depends(get_collection)):
    # return  "user logged hey in"
    print("user details fetched",token)
    
    # payload = verify_token(token)
    # print(payload,"payload")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = await collection.find_one({"email": token.get("user", {}).get("email")})
    print(user,"user")
    
    if user:
        return{
            "id":str(user['_id']),
            "name":user['name'],
            "email":user['email'],
            "role":user['role']

        }

    if user is None:
        raise InvalidCredentials

        #raise HTTPException(status_code=404, detail="User not found")
   
class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
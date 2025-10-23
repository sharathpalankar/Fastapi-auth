from typing import Any, List
from auth import verify_token
from fastapi import Depends, Request,HTTPException,status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
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

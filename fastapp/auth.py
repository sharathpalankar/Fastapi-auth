from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(
    user_data: dict, expiry: timedelta =None, refresh: bool = False 
):
    to_encode = {}

    to_encode["user"] = user_data
    to_encode["exp"] = datetime.utcnow() + (
        expiry if expiry is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES )
    )

    to_encode["refresh"] = refresh

    print("to encode data is",to_encode)

    token = jwt.encode(
        to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )

    return token

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     print(to_encode)
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def create_refresh_token(data: dict, expiry: timedelta = None, refresh: bool = False):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
#     to_encode.update({"exp": expire,"refresh": refresh})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try: 
        print("Current token:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)

        # print("the payload is",payload)
        return payload
    except JWTError as e:
        print("Token verification error:", str(e))
        return None
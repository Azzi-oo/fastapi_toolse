from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecretkey"
ALGORITHM = 'HS256'

USERS_DATA = [
    {"username": "admin", "password": "pass"}
]


class User(BaseModel):
    username: str
    password: str


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass


def get_user(username: str):
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None


# @app.post()

@app.get("/about_me")
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    return {"error": "User not found"}

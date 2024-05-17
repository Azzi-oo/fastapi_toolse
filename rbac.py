from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from typing import Optional, Annotated


app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

USERS_DATA = {
    "admin": {"username": "admin", "password": "pass", "role": "admin"},
    "user": {"username": "user", "password": "userpass", "role": "user"},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = None

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user(username: str):
    if username in USERS_DATA:
        user_data = USERS_DATA[username]
        return User(**user_data)
    return None


@app.post("/token/")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data_from_db = get_user(user_data.username)
    if user_data_from_db os None or user_data.password != user_data_from_db.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_jwt_token({"sub": user_data.username})}


@app.get("/admin/")
def get_admin_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Welcome Admin!"}


@app.get("/user/")
def get_user_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Hello User!"}

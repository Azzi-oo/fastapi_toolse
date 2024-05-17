from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


fake_user = {
    1: {"username": "john_doe"},
    2: {"username": "jane_smith"},
}


@app.get("/users/{user_id}")
def read_user(user_id):
    if user_id in fake_user:
        return fake_user[user_id]
    return {"error": "User not found"}


@app.get("/users/")
def read_users(limit: int = 10):
    return dict(list(fake_user.items())[:limit])
# class User(BaseModel):
#     username: str
#     user_info: str

# fake_db = [{"username": "vasya", "user_info": "love kolbasy"}, {"username": "katya", "user_info": "love song"}]


# @app.get('/users')
# async def get_all_users():
#     return fake_db


# @app.post('/add_user')
# async def add_user(user: User):
#     fake_db.append({'username': user.username, 'user_info': user.user_info})
#     return {'message': 'user add in db'}

# from fastapi import FastAPI
# from pydantic import BaseModel
# app = FastAPI()


# class User(BaseModel):
#     username: str
#     message: str


# @app.post("/")
# async def root(user: User):
#     return {f"message {user.message}): {user.username}"}


# @app.get("/custom")
# def read_custom_message():
#     return {'message': 'This is a custom message!'}

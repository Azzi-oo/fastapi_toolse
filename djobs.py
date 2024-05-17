from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

DATABASE_URL = ''

database = Database(DATABASE_URL)


class UserCreate(BaseModel):
    username: str
    email: str


class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None


@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    values = {"username": user.username, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")


#  маршрут для получения инфы о юзере по ИД
@app.get("/user/{user_id}", response_model=UserReturn)
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch user from database")
    if result:
        return UserReturn(username=result["username"], email=result["email"])
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

@app.put("/user/{user_id}", response_model=UserReturn)
async def update_user(user_id: int, user: UserCreate):
    query = "UPDATE users SET username = :username, email = :email WHERE id = :user_id"
    values = {"user_id": user_id, "username": user.username, "email": user.email}
    try:
        await database.execute(query=query, values=values)
        return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update user in database")
from fastapi import FastAPI, Cookie, Response, Header
from pydantic import BaseModel
from typing import Union, Annotated
from datetime import datetime


class Item(BaseModel):
    name: str
    description: Union[str, None]
    price: float
    tax: Union[float, None] = None


app = FastAPI()

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


@app.get("/items")
async def read_items1(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}


@app.get("/")
def root(response: Response):
    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    response.set_cookie(key="last_login", value=now)
    return {"message": "cookie installed"}


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.post("/items/")
async def create_item(item: Item):
    return item

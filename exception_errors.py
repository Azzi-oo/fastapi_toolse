from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)


class Item(BaseModel):
    name: str
    description: Union[str, None]
    price: float
    tax: Union[float, None] = None


app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3")
    return {"item_id": item_id}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": 'There goes my error'},
        )
    return {"item": items[item_id]}


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"error":str(exc)})


@app.post("/items/")
async def create_item(item: Item):
    try:
        if item.price < 0:
            raise ValueError("Price must be non-negative")
        return {"message": 'Item created successfully', 'item': item}
    except ValueError as ve:
        raise ve

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class ItemsResponse(BaseModel):
    item_id: int


class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_details: str


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    error = jsonable_encoder(CustomExceptionModel(status_code=exc.status_code, er_message=exc.message, er_details=exc.detail))
    return JSONResponse(status_code=exc.status_code, content=error)


@app.get("/items/{item_id}/", response_model=ItemsResponse)
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail="Item not found", status_code=404)
    return ItemsResponse(item_id=item_id)


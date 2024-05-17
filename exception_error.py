from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
app = FastAPI()


class CustomExceprion(HTTPException):
    def __init__(self, status_code: int = 400, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(CustomExceprion)
async def custom_exception_handler(request: Request, exc: CustomExceprion):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomExceprion(detail="Item not found", status_code=404)
    return {"item_id": item_id}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'error': 'Internal server error'}
    )


@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    result = 1 / 0
    return {"item_id": item_id}

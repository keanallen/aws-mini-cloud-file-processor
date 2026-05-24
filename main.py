from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.api.router import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(map(str, error["loc"])),
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors
        }
    )
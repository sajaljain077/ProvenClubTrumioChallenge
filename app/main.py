from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request
from fastapi.exceptions import RequestValidationError
from .database import SessionLocal, engine
from app.controller import libraryController
from starlette.responses import JSONResponse
from app import schema
from app.utils.utils import responseMaker, errorMaker
import uuid


app = FastAPI()

# Define the root endpoint
@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={"message": "This is the backend for Library Service"})




@app.exception_handler(RequestValidationError)
async def validationExceptionhandler(request:Request, exc:RequestValidationError):
    """
    Exception handler for handling validation errors.

    Args:
        request: FastAPI Request object.
        exc: Instance of RequestValidationError.

    Returns:
        JSON response with validation error details.
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    inputValidationError = []
    for error in exc.errors():
        if error["type"] =="missing" and error["loc"][0] == "query":
            inputValidationError.append(await errorMaker("inputvalidationError", f"Query Parameter {error['loc'][-1]}",  "is required"))
        else:
            inputValidationError.append(await errorMaker("inputvalidationError", error['loc'][-1], error['msg']))
    return await responseMaker(requestId=requestId, errors=inputValidationError, statusCode=400)


# Include routers for address and user controllers
app.include_router(libraryController.router, prefix="/library/v1", tags=["Library Router"])


# Create database tables based on the defined schema
schema.Base.metadata.create_all(bind=engine)
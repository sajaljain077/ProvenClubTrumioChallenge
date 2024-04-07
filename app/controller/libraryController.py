from app.database import get_db
from app.model.requestModel import libraryModel
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.service.crudOperation import *
import uuid
from app.service.crudOperation import issueBook, returnBook
import sys
# from app.utils.log import logger

router = APIRouter()


@router.post("/issueBook")
async def issueBookToMember(request:Request, payload : libraryModel, dbConn:Session()=Depends(get_db)): # type: ignore
    """
    Endpoint for issue a book.

    Args:
        request: FastAPI Request object.
        payload: library model representing requested book data.
        dbConn: Database session dependency.    

    Returns:
        Response with information about the issued book
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    payload = jsonable_encoder(payload)
    response = await issueBook(dbConn, payload, requestId)
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return response



@router.post("/returnBook")
async def returnBookToLibrary(request:Request, payload : libraryModel, dbConn:Session()=Depends(get_db), ): # type: ignore
    """
    Endpoint for return a book.

    Args:
        request: FastAPI Request object.
        payload: library model representing returning book data.
        dbConn: Database session dependency.

    Returns:
        Response with information about returned book
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    payload = jsonable_encoder(payload)
    response = await returnBook(dbConn, payload, requestId)
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return response


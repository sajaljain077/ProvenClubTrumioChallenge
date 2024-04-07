from app.schema import Books, Members, CirculationHistory, ReservationQueue
from app.utils.utils import errorMaker, responseMaker
from datetime import datetime
from datetime import datetime, timedelta, timezone
from fastapi.encoders import jsonable_encoder
from app.utils.log import logger





async def issueBook(dbConn, payload, requestId):
    """
        Function to check whether book exist or not if exist then return it
        Args:
            requestid, db connection, payload

        Returns:
            Access Token
    """
    askedBook = dbConn.query(Books).filter(Books.bookId == payload["bookId"])
    if askedBook.first():
        if jsonable_encoder(askedBook.first())["remainingCopies"] > 0:
            try:
                askedBook.update({"remainingCopies":jsonable_encoder(askedBook.first())["remainingCopies"]-1})
                circualtionData = CirculationHistory(bookId = payload["bookId"], memberId = payload["memberId"], issuedDate = datetime.now(), status = "onRent")
                dbConn.add(circualtionData)
                dbConn.commit()
                return await responseMaker(statusCode=200, requestId=requestId, errors=[], data=f"BookId {payload['bookId']} has been given to member {payload['memberId']}")
            except Exception as err:
                return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("somethingwentwrong", err)])
        else:
            try:
                reservationQueueData = ReservationQueue(bookId = payload["bookId"], memberId = payload["memberId"], reservationTime = datetime.now(), status = "pending")
                dbConn.add(reservationQueueData)
                dbConn.commit()
            except Exception as err:
                return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("somethingwentwrong", err)])
            return await responseMaker(statusCode = 400, requestId=requestId, errors=[await errorMaker("outOfStock")], data={})
    else:
        return await responseMaker(statusCode = 400, requestId=requestId, errors=[await errorMaker("invalidBookId", payload["bookId"])], data={})
    
async def returnBook(dbConn, payload, requestId):
    """
        Function to check whether log in user is valid or not
        Args:
            requestid, db connection, payload

        Returns:
            returned book information
    """
    returningBookData = dbConn.query(CirculationHistory).filter(CirculationHistory.bookId == payload["bookId"], CirculationHistory.memberId == payload["memberId"])
    if returningBookData.first():
        try:
            returningBookData.update({"returnedDate":datetime.now(), "status":"returned"})
            bookData = dbConn.query(Books).filter(Books.bookId == payload["bookId"])
            remainingCopies = jsonable_encoder(bookData.first())["remainingCopies"]
            bookData.update({"remainingCopies":remainingCopies+1})
            dbConn.commit()
            """
            Here we can also send the message to user who has made reservation to the that book
            """
            return await responseMaker(statusCode=200, requestId=requestId, errors=[], data=f"BookId {payload['bookId']} has been retirned succesfully by member - {payload['memberId']}")
        except Exception as err:
            return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("somethingwentwrong", err)])
    else:
        return await responseMaker(statusCode = 400, requestId=requestId, errors=[await errorMaker("invalidBookIdandMemberid", payload["bookId"], payload["memberId"])], data={})
    
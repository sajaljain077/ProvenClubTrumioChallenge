from starlette.responses import JSONResponse
from app.utils.errors import LIBRARYERROR
import hashlib
import hmac




async def responseMaker(requestId, errors = [], data = {}, statusCode = 200):
    resp = {}
    resp["requestId"] = requestId
    resp["errors"] = errors
    resp["data"] = data

    return JSONResponse(status_code=statusCode, content=resp)


async def errorMaker(id, *arguments):
    arguments = [i for i in arguments]
    if len(arguments) == 1:
        return {
            "errorCode":id,
            "errorMsg":LIBRARYERROR[id]%arguments[0]
        }
    else:
        arguments = tuple(arguments)
        return {
            "errorCode":id,
            "errorMsg":LIBRARYERROR[id]%arguments
        }
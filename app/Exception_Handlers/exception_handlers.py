from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from Models.models import InternalServerErrorModel, Error404Model
from Log.logger import log

def exception_handler(request: Request, exec: Exception):
    log.error(exec, stack_info=True)    
    return JSONResponse(
        content=InternalServerErrorModel().model_dump(), 
        status_code=500)

def http_exception_handler(request: Request, exec: HTTPException):
    log.error(exec, stack_info=True)
    if exec.status_code == 404:
        return JSONResponse(
            content=Error404Model(message=exec.detail).model_dump(), 
            status_code=404)
    if exec.status_code == 500:
        return JSONResponse(
            content=InternalServerErrorModel(message=exec.detail).model_dump(), 
            status_code=500)
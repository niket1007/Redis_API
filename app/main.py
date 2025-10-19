from fastapi import FastAPI, HTTPException
from Routers.routers import router
from Exception_Handlers.exception_handlers import (
    exception_handler, http_exception_handler)

app = FastAPI(debug=False)

app.include_router(router)
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

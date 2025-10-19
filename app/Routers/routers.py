from fastapi import APIRouter, Depends, Query, Path
from Redis.redis import Redis, init_connection, ping, get_data, set_data, delete_key
from typing import Annotated, Optional
from Models.models import *
from Log.logger import log

redis_dep = Annotated[Redis, Depends(init_connection)]

router = APIRouter(responses={
    500: {"model": InternalServerErrorModel},
    404: {"model": Error404Model}
})

@router.get(
        path="/ping", 
        response_model=PingResponseModel, 
        status_code=200)
async def ping_redis(conn: redis_dep):
    log.info("Started ping_redis")
    result = ping(conn=conn)
    log.debug(f"After calling ping function, output is {str(result)}")
    log.info("Ended ping redis")
    return PingResponseModel(status="success" if result else "failure")

@router.get(
    path="/redis/{key}",
    status_code=200,
    response_model=GETResponseModel
)
async def get_redis_data(
    conn: redis_dep, 
    key: str = Path(description="Redis Key"),
    path: Optional[str] = Query(
        description="Only valid for hash, json", default=None)):
    log.info("Started get_redis_data")
    value = get_data(conn, key, path)
    log.debug(f"After calling get_data function, output is {str(value)}")
    log.info("Ended get_redis_data")
    return GETResponseModel(key=key, value=value) 

@router.post(
    path="/redis",
    status_code=201,
    response_model=SETResponseModel)
async def set_redis_data(
    conn: redis_dep,
    body: SETRequestModel):
    log.info("Started set_redis_data")
    set_data(conn, body)
    log.debug(f"After calling set_data function")
    log.info("Ended set_redis_data")
    return SETResponseModel(
        key=body.key, 
        message="Successfully added/updated to redis")

@router.delete(
    path="/redis/{key}",
    status_code=202,
    response_model=DeleteResponseModel)
async def delete_redis_key(
    conn: redis_dep,
    key: str = Path(description="Redis Key")):
    log.info("Started delete_redis_key")
    delete_key(conn, key)
    log.debug(f"After calling delete_key function")
    log.info("Ended delete_redis_key")
    return DeleteResponseModel(key=key)
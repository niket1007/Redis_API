from redis import Redis
from Log.logger import log
from decouple import config
from typing import Generator, Any, Optional
from fastapi.exceptions import HTTPException
from Models.models import DataTypeEnum, SETRequestModel

def init_connection() -> Generator[Redis]:
    redis = None
    try:
        redis = Redis(
            host=config("redis_host", cast=str),
            port=config("redis_port", cast=int),
            username=config("redis_username", cast=str, default=None),
            password=config("redis_password", cast=str, default=None),
            decode_responses=True
        )
        yield redis
    except Exception as e:
        raise e
    finally:
        if redis:
            redis.close()

def ping(conn: Redis) -> bool:
    try:
        return conn.ping()
    except Exception as e:
        log.error(e)
        return False

def get_key_datatype(conn: Redis, key: str) -> str:
    return conn.type(key).upper()

def check_key_exist(conn: Redis, key: str) -> bool:
    return conn.exists(key)

def get_str_data(conn: Redis, key: str) -> Optional[str]:
    return conn.get(name=key)

def set_str_data(
        conn: Redis, 
        key: str, value: str, expiryTime: Optional[int] = None) -> None:
    if expiryTime is not None:
        return conn.set(name=key, value=value, ex=expiryTime)
    conn.set(name=key, value=value)

def get_list_data(conn: Redis, key: str) -> Optional[list[Any]]:
    return conn.lrange(name=key, start=0, end=-1)

def set_list_data(
        conn: Redis, 
        key: str, values: list, expiryTime: Optional[int] = None) -> None:
    pipe = conn.pipeline(transaction=True)
    for value in values:
        pipe.rpush(key, value)
    if expiryTime is not None:
        pipe.expire(key, expiryTime)
    pipe.execute()

def get_set_data(conn: Redis, key: str) -> Optional[set]:
    set_length = conn.scard(name=key)
    return conn.srandmember(name=key, number=set_length)

def set_sets_data(
        conn: Redis, 
        key: str, values: set, expiryTime: Optional[int] = None) -> None:
    pipe = conn.pipeline(transaction=True)
    for value in values:
        pipe.sadd(key, value)
    if expiryTime is not None:
        pipe.expire(key, expiryTime)
    pipe.execute()

def get_hash_data(conn: Redis, key: str, path: Optional[str] = None) -> Optional[str|dict]:
    if path:
        return conn.hget(name=key, key=path)
    return conn.hgetall(name=key)

def set_hash_data(
        conn: Redis, 
        key: str, value: dict, expiryTime: Optional[int] = None) -> None:
    pipe = conn.pipeline(transaction=True)
    pipe.hset(name=key, mapping=value)
    if expiryTime is not None:
        pipe.expire(key, expiryTime)
    pipe.execute()

def get_json_data(conn: Redis, key: str, path: Optional[str] = None) -> Optional[dict]:
    if path:
        return conn.json().get(key, path)
    return conn.json().get(name=key)

def set_json_data(
        conn: Redis, 
        key: str, value: dict, path: Optional[str], expiryTime: Optional[int] = None) -> None:
    if path is None:
        path = "$"
    pipe = conn.pipeline(transaction=True)
    pipe.json().set(name=key, path=path, obj=value)
    if expiryTime is not None:
        pipe.expire(key, expiryTime)
    pipe.execute()

def get_data(
        conn: Redis, 
        key: str, path: Optional[str] = None) -> Any:
    if check_key_exist(conn, key):
        datatype = get_key_datatype(conn, key)
        if datatype == "HASH":
            return get_hash_data(conn, key, path)
        elif datatype == "STRING":
            return get_str_data(conn, key)
        elif datatype == "LIST":
            return get_list_data(conn, key)
        elif datatype == "SET":
            return get_set_data(conn, key)
        elif datatype == "REJSON-RL":
            return get_json_data(conn, key, path)
        else:
            raise HTTPException(status_code=500, detail="Invalid datatype")
    else:
        raise HTTPException(status_code=404, detail="Invalid key")

def set_data(
        conn: Redis,
        body: SETRequestModel) -> None:
    if body.data_type == DataTypeEnum.string:
        set_str_data(conn, body.key, body.value, body.expiryT)
    elif body.data_type == DataTypeEnum.lists:
        set_list_data(conn, body.key, body.value, body.expiryT)
    elif body.data_type == DataTypeEnum.sets:
        set_sets_data(conn, body.key, body.value, body.expiryT)
    elif body.data_type == DataTypeEnum.hash:
        set_hash_data(conn, body.key, body.value, body.expiryT)
    elif body.data_type == DataTypeEnum.json:
        set_json_data(conn, body.key, body.value, body.json_path, body.expiryT)
    else:
        raise HTTPException(status_code=500, detail="Invalid datatype")

def delete_key(conn: Redis, key: str) -> None:
    if check_key_exist(conn, key):
        conn.delete(key)
    else:
        raise HTTPException(status_code=404, detail="Invalid key")

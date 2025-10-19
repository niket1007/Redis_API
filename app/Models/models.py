from pydantic import BaseModel, Field, model_validator
from typing import Any, Optional
from enum import Enum

class InternalServerErrorModel(BaseModel):
    status: str = "error"
    message: str = Field(default="Check server logs for debugging the issue")

class PingResponseModel(BaseModel):
    status: str = Field(
        description="Redis server ping status", 
        examples=[
            "success",
            "failure"
        ])

class Error404Model(BaseModel):
    message: str = Field(description="404 error message")

class GETResponseModel(BaseModel):
    key: str = Field(description="Redis key")
    value: Any = Field(description="Redis value")

class DataTypeEnum(Enum):
    lists = "LIST"
    sets = "SET"
    hash = "HASH"
    string = "STRING"
    json = "JSON"

class SETRequestModel(BaseModel):
    data_type: DataTypeEnum = Field(description="Redis key datatype")
    key: str = Field(description="Redis key")
    value: Any = Field(description="Redis value")
    expiryT: Optional[int] = Field(
        description="Key expiry time in seconds", default=None)
    json_path: Optional[str] = Field(
        description="Valid only for json", default=None)
    
    @model_validator(mode='after')
    def validate_data_type(self):
        if (self.data_type == DataTypeEnum.string and 
            not isinstance(self.value, str)):
                raise ValueError("Value should be of string datatype")
        elif (self.data_type == DataTypeEnum.hash and
            not isinstance(self.value, dict)):
                raise ValueError("Value should be of dict datatype")
        elif (self.data_type == DataTypeEnum.json and
            not isinstance(self.value, dict)):
                raise ValueError("Value should be of dict datatype")
        elif (self.data_type == DataTypeEnum.lists and
            not isinstance(self.value, list)):
                raise ValueError("Value should be of list datatype")
        elif (self.data_type == DataTypeEnum.sets and 
            not isinstance(self.value, list)):
                raise ValueError("Value should be of list datatype")
        return self

class SETResponseModel(BaseModel):
    key: str = Field(description="Redis key")
    message: str = Field(description="create/update operation message")

class DeleteResponseModel(BaseModel):
    key: str = Field(description="Redis key")
    message: str = "Delete operation successfully completed" 
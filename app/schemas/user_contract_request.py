from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    content : str
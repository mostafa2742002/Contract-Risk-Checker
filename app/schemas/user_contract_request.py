from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    contract : str
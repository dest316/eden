from pydantic import BaseModel


class LoginRequestBody(BaseModel):
    login: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class SignupRequestBody(LoginRequestBody):
    nickname: str


class SignupResponse(LoginResponse):
    ...

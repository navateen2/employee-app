from pydantic import BaseModel,ConfigDict


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    id: int
    email: str
    role: str

class RefreshTokenPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    refresh_token: str
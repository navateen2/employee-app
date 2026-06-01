from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import service as auth_service
from auth.schemas import TokenResponse,RefreshTokenPayload
from fastapi.security import OAuth2PasswordRequestForm
from database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    token = await auth_service.login(db, body.username, body.password)
    return TokenResponse(access_token=token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token_auth(
    payload: RefreshTokenPayload, db: Session = Depends(get_db)
):

    new_access_token, new_refresh_token = await auth_service.refresh_token(
        db, payload.refresh_token
    )

    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
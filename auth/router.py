from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import service as auth_service
from auth.schemas import LoginRequest, TokenResponse
from database.connection import get_db

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/login",response_model=TokenResponse)
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    token = await auth_service.login(db,body.email, body.password)
    return TokenResponse(access_token=token)


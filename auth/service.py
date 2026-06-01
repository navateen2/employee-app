from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import UnauthorizedException
from repositories import employee_repo
import logging
from auth.utils import decode_token 
from auth.utils import verify_password, create_access_token,create_refresh_token

logger = logging.getLogger(__name__)


async def login(db: AsyncSession, email: str, password: str) -> str:
    employee = await employee_repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    logger.info(f"User {email} logged in successfully")
    return create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )

async def refresh_token(db: AsyncSession, refresh_token: str) -> tuple[str, str]:

    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh_token":
        raise UnauthorizedException(
            detail="Invalid or expired refresh token, needs to reauthenticate"
        )

    new_payload = {
        "id": payload.get("id"),
        "email": payload.get("email"),
        "role": payload.get("role"),
    }

    new_access_token = create_access_token(new_payload)
    new_refresh_token = create_refresh_token(new_payload)

    return new_access_token, new_refresh_token
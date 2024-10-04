from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.const import auth_params
from app.database.session import get_db_session

from app.schemas.auth import TokenSchema
from app.services.auth import AuthService

router = APIRouter(**auth_params)

@router.post("")
async def authenticate(
    login: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session)
    ) -> TokenSchema | None:
    """User authentication.

    Raises:
        HTTPException: 401 Unauthorized
        HTTPException: 404 Not Found

    Returns:
        Access token.
    """
    return AuthService(session).authenticate(login)
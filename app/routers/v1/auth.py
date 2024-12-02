from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.const import auth_params
from app.database.session import get_db_session

from app.schemas.auth import TokenSchema, CreateUserSchema
from app.services.auth import AuthService

router = APIRouter(**auth_params)

@router.post("/create")
async def create_user(
    name: str,
    email: str,
    password: str,
    session: AsyncSession = Depends(get_db_session)
    ) -> None:
    """Create new user.

    Raises:
        HTTPException: 400 Bad Request

    Returns:
        None
    """
    await AuthService(session).create_user(
        CreateUserSchema(name=name, email=email, password=password)
)

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
    return await AuthService(session).authenticate(login)


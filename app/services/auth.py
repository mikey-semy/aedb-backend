from datetime import datetime, timedelta


from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jwt import encode, decode, PyJWTError
from sqlalchemy import select
from passlib.context import CryptContext

from app.schemas.auth import UserSchema, CreateUserSchema, TokenSchema
from app.services.base import BaseService, BaseDataManager
from app.models.auth import UserModel
from app.utils.exc import raise_with_log
from app.const import (
    auth_url,
    token_type,
    token_algorithm,
    token_expire_minutes,
)
from app.core.config import config

oauth2_schema = OAuth2PasswordBearer(tokenUrl=auth_url, auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashingMixin:
    """Hashing and verifying passwords."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Generate a bcrypt hashed password."""

        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verify a password against a hash."""

        return pwd_context.verify(plain_password, hashed_password)
    
class AuthService(HashingMixin, BaseService):

    def create_user(self, user: CreateUserSchema) -> None:
        
        user_model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=self.bcrypt(user.password)
        )
        AuthDataManager(self.session).add_user(user_model)
        
    def authenticate(
            self, login: OAuth2PasswordRequestForm = Depends()
    ):
        user = AuthDataManager(self.session).get_user(login.username)

        if user.hashed_password is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
        else:
            if not self.verify(user.hashed_password, login.password):
                raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
            else:
                access_token = self._create_access_token(user.name, user.email)
                return TokenSchema(access_token=access_token, token_type=token_type)
        return None
    
    def _create_access_token(self, name: str, email: str) -> str:
        
        payload = {
            "name": name,
            "sub": email,
            "expires_at": self._expiration_time()
        }
        
        return encode(payload=payload,
                      key=config.token_key.get_secret_value(),
                      algorithm=token_algorithm)
    
    @staticmethod
    def _expiration_time() -> str:
        """Get token expiration time."""

        expires_at = datetime.now(datetime.datetime.UTC) + timedelta(minutes=token_expire_minutes)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")
    
class AuthDataManager(BaseDataManager):
    def add_user(self, user: UserModel) -> None:
        """Add user to tadabase."""
        self.add_one(user)
    
    def get_user(self, email: str) -> UserSchema:

        model = self.get_one(select(UserModel).where(UserModel.email == email))

        if not isinstance(model, UserModel):
            raise_with_log(status.HTTP_404_NOT_FOUND, "User not found")

        return UserSchema(
            name=model.name,
            email=model.email,
            hashed_password=model.hashed_password
        )


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    """Decode token to obtain user information.

    Extracts user information from token and verifies expiration time.
    If token is valid then instance of :class:`~app.schemas.auth.UserSchema`
    is returned, otherwise exception is raised.

    Args:
        token:
            The token to verify.

    Returns:
        Decoded user dictionary.
    """

    if token is None:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    try:
        # decode token using secret token key provided by config
        payload = decode(jwt=token,
                         key=config.token_key.get_secret_value(),
                         algorithms=[token_algorithm])

        # extract encoded information
        name: str = payload.get("name")
        sub: str = payload.get("sub")
        expires_at: str = payload.get("expires_at")

        if sub is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return UserSchema(name=name, email=sub)
    except PyJWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    return None


def is_expired(expires_at: str) -> bool:
    """Return :obj:`True` if token has expired."""
    
    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.now(datetime.UTC)
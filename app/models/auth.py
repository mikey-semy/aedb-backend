from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel
from app.models.posts import PostModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.posts import PostModel
    
class UserModel(SQLModel):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    email: Mapped[str] = mapped_column("email", unique=True, nullable=False)
    name: Mapped[str] = mapped_column("name")
    hashed_password: Mapped[str] = mapped_column("hashed_password")

    posts: Mapped[List["PostModel"]] = relationship(
        # default_factory=list,
        back_populates="author",
        lazy='joined',
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView
from app.core.config import config

from sqlalchemy.ext.asyncio import create_async_engine

from app.models.manuals import (
    CategoryModel, 
    GroupModel, 
    ManualModel
    )
from app.models.auth import UserModel
from app.models.posts import PostModel

app = FastAPI()
async_engine = create_async_engine(config.dsn, echo=True)

admin = Admin(
    engine = async_engine,
    title="Admin Panel",
    base_url="/admin",
)

admin.add_view(ModelView(CategoryModel))
admin.add_view(ModelView(GroupModel))
admin.add_view(ModelView(ManualModel))
admin.add_view(ModelView(UserModel))
admin.add_view(ModelView(PostModel))

admin.mount_to(app)

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.posts import PostModel
from app.schemas.posts import PostSchema
from app.services.base import BaseService, BaseDataManager

class PostService(BaseService):
    def get_post(self, post_id: int) -> PostSchema:
        return PostDataManager(self.session).get_post(post_id)

    def get_posts(self) -> List[PostSchema]:
        return PostDataManager(self.session).get_posts()


class PostDataManager(BaseDataManager):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, PostSchema)
        
    def get_post(self, post_id: int) -> PostSchema:
        statement = select(PostModel).where(PostModel.id == post_id)
        return self.get_one(statement)

    def get_posts(self) -> List[PostSchema]:
        schemas: List[PostSchema] = list()
        statement = select(PostModel)
        for model in self.get_all(statement):
            schemas.append(PostSchema(**model.to_dict()))
        return schemas

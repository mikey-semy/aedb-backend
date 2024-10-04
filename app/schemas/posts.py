from datetime import datetime
from app.schemas.base import BaseSchema

class PostSchema(BaseSchema):
    ''' This is the base class for post-related schemas. '''
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    title: str
    description: str

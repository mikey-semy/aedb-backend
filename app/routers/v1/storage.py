# from typing import List
# from fastapi import APIRouter
# from app.services.auth import get_current_user
# from app.database.session import get_db_session
# from app.schemas.auth import UserSchema
# from app.schemas.storage import StorageSchema
# from app.services.storage import StorageService
# from app.const import storage_params

# router = APIRouter(**storage_params)

# @router.get("/")
# async def get_storage() -> List[StorageSchema]:
#     _user: UserSchema = Depends(get_current_user)
#     session: Session = Depends(get_db_session)
#     return await StorageService(session).get_storage()
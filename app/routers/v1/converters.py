# from fastapi import APIRouter
# from app.services.auth import get_current_user
# from app.database.session import get_db_session
# from app.schemas.auth import UserSchema
# from app.schemas.converters import ConverterSchema
# from app.services.converters import ConverterService
# from app.const import converters_params

# router = APIRouter(**converters_params)

# @router.get("/")
# async def get_converters() -> List[ConverterSchema]:
#     _user: UserSchema = Depends(get_current_user)
#     session: Session = Depends(get_db_session)
#     return await ConverterService(session).get_converters()
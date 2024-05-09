from sqlalchemy.ext.asyncio import AsyncSession

from src.common.configs import pwd_context
from src.common.exception import NotUniqueError
from src.db.query import user_crud

from ..model import user_request


async def verify_user(
    *,
    db: AsyncSession,
    user: user_request.UserCreateRequest,
) -> None:
    user_list = await user_crud.read_user_by_name_email(
        db=db,
        name=user.name,
        email=user.email,
    )

    username_conflict = [u for u in user_list if user.name == u.name]
    if username_conflict:
        raise NotUniqueError(field=user.name)

    email_conflict = [u for u in user_list if user.email == u.email]
    if email_conflict:
        raise NotUniqueError(field=user.email)


async def create_user(
    *,
    db: AsyncSession,
    user_create: user_request.UserCreateRequest,
) -> None:
    await user_crud.create_user(
        db=db,
        name=user_create.name,
        password=pwd_context.hash(user_create.password1),
        email=user_create.email,
    )

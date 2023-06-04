from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from settings.database import get_db
from src.schemas.common.user import *
from src.crud.common.user import *

router = APIRouter(
    prefix="/api/user",
)


@router.put("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_existing_user(db, user_create)
    conflict_email = [u for u in existing_user if u.email == user_create.email]
    conflict_username = [u for u in existing_user if u.username == user_create.username]
    if conflict_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email conflict"
        )
    elif conflict_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username conflict"
        )
    create_user(db, user_create)
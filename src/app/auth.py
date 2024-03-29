from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jose import jwt, JWTError

from conf.database import get_db
from conf.config import get_key
from src.crud import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/login')


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    auth_config = get_key().auth
    try:
        payload = jwt.decode(token, auth_config.secret_key, auth_config.algorithm)
        username: str = str(payload.get('sub'))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = await get_user(db, username)
        if user is None:
            raise credentials_exception
        return user
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Annotated

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        if not token:
            return 0
        payload = jwt.decode(token, options={"verify_signature": False, "verify_exp": True})
        user_id = payload.get("user_id")
        if user_id is None:
            return 0
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise e
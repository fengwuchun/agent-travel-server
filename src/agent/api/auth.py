from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from agent.utils.jwt_util import JwtUtil
import jwt


security = HTTPBearer()


def get_current_user(
    credentials=Depends(security)
):
    token = credentials.credentials

    try:

        payload = JwtUtil.parse_token(token)

        return {
            "user_id": payload["id"],
            "username": payload["sub"],
            "role": payload["role"]
        }

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
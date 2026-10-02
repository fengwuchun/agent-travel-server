import jwt
from typing import Optional


class JwtUtil:

    SECRET_KEY = "city-system-jwt-secret-key-20260722-abcdef"
    ALGORITHM = "HS256"

    @classmethod
    def parse_token(cls, token: str) -> dict:
        """
        验证并解析 JWT。

        会自动验证：
        1. JWT 签名
        2. Token 是否过期
        3. Token 格式
        """
        return jwt.decode(
            token,
            cls.SECRET_KEY,
            algorithms=[cls.ALGORITHM]
        )

    @classmethod
    def parse_username(cls, token: str) -> str:
        payload = cls.parse_token(token)
        return payload["sub"]

    @classmethod
    def parse_role(cls, token: str) -> str:
        payload = cls.parse_token(token)
        return payload["role"]

    @classmethod
    def parse_id(cls, token: str) -> int:
        payload = cls.parse_token(token)
        return payload["id"]

    @classmethod
    def get_remaining_seconds(cls, token: str) -> int:
        payload = cls.parse_token(token)

        exp = payload.get("exp")

        if exp is None:
            return 0

        import time

        remaining = int(exp - time.time())

        return max(remaining, 0)
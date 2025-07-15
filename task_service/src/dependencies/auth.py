from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient, ConnectError

from src.core.config import AUTH_SERVICE_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    async with AsyncClient() as client:
        try:
            assert AUTH_SERVICE_URL is not None, "AUTH_SERVICE_URL is not set"
            response = await client.get(
                f'{AUTH_SERVICE_URL}/auth/me',
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                )
            return response.json()
        except ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service unavailable",
            )



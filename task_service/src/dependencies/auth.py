from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient, ConnectError, ReadError, TimeoutException

from src.core.config import AUTH_SERVICE_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/auth/login") # нужно указывать localhost, что авторизация через Swager UI работала.

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
        except (ConnectError, ReadError, TimeoutException) as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Auth service unavailable: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            )



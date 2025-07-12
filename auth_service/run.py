import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy import text

# from src.core.config import DATABASE_URL


# async def test_connection():
#     # Убедитесь, что URL правильный (без лишних параметров)

    
#     engine: AsyncEngine = create_async_engine(DATABASE_URL) # type: ignore
    
#     try:
#         async with AsyncSession(engine) as session:
#             # Правильный способ выполнения запроса
#             result = await session.execute(text("SELECT 1"))
#             print("Connection successful! Result:", result.scalar())
#     except Exception as e:
#         print(f"Connection failed: {e}")
#     finally:
#         await engine.dispose()

# asyncio.run(test_connection())
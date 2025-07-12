from src.models.user import User
from src.db.session import engine, Base

Base.metadata.create_all(bind=engine)

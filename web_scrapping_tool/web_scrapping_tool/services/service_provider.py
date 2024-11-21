from fastapi import Depends
from ..db.mongo import get_db
from .user import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
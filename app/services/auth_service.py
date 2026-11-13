from typing import Optional
from sqlmodel import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password

class AuthService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def register_user(self, username: str, password: str) -> Optional[User]:
        if self.repo.get_by_username(username):
            return None
        hashed = hash_password(password)
        new_user = User(username=username, hashed_password=hashed)
        return self.repo.create(new_user)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
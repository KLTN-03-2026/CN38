from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.user import User
from ..schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        hashed = self.hash_password(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed,
            full_name=user_data.full_name,
            phone=user_data.phone,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            sub = payload.get("sub")
            if sub is None:
                return None
            return str(sub)
        except JWTError:
            return None

from sqlalchemy import (
    Column,
    Integer,
    String,
)

from src.db.config import Base
from src.auth import utils


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    salt = Column(String(200))
    email = Column(String(200), unique=True, index=True)
    username = Column(String(200), unique=True, index=True)
    role = Column(String(200))

    def check_password(self, password: str) -> bool:
        return utils.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = utils.generate_salt()
        self.hashed_password = utils.get_password_hash(self.salt + password)

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .main import db

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = True)
    email: Mapped[str] = mapped_column(unique = True, nullable = True)
    password: Mapped[str] = mapped_column(nullable = True)
    role: Mapped[str] = mapped_column(nullable = True, default = "User")

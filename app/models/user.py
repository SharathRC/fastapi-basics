from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), index=True, nullable=True)
    email = Column(String(256), nullable=False)
    is_superuser = Column(Boolean, default=False)
    recipes = relationship(
        "Recipe",
        cascade="all, delete-orphan",  # delete all child (recipes) when a user is deleted
        back_populates="submitter",
        uselist=True,
    )

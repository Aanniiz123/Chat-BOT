from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prompt = Column(Text, nullable=False)
    title = Column(String(255), nullable=False, default="New chat")
    role = Column(String(50), nullable=False, default="user")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ai_response = Column(Text, nullable=False)
    model_name = Column(String(255), nullable=True)
    search_results = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f"Agent(id={self.id}, title={self.title!r}, role={self.role!r}, "
            f"created_at={self.created_at!r})"
        )
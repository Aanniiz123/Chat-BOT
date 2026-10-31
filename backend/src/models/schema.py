
from pydantic import BaseModel, Field
from typing import Optional, Literal


class AgentConfig(BaseModel):
    prompt: str = Field(..., min_length=1)
    model_name: Optional[str] = None
    title: str = "New chat"
    role: Literal["user", "assistant"] = "user"

class AgentTitleUpdate(BaseModel):
    title : str

class AgentConversationDelete(BaseModel):
    id : str
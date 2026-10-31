
from typing import List
from langchain_protocol import TypedDict


class AgentState(TypedDict):
    prompt: str
    ai_response: str
    agent: str
    search_results: List[str]

import os
from typing import Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from core.logger import logger

load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
llm_model: ChatGroq | None = None


def _get_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API")
    if not api_key:
        logger.warning("GROQ API key is not set. Set GROQ_API_KEY or GROQ_API in your environment/.env file.")
    return api_key


def get_llm(model_name: str | None = None, **kwargs) -> ChatGroq:
    """Create or return a shared Groq LLM instance."""
    global llm_model

    api_key = _get_api_key()
    if not api_key:
        raise ValueError("Missing GROQ API key. Add GROQ_API_KEY or GROQ_API to your environment.")

    selected_model = model_name or DEFAULT_MODEL

    if llm_model is None or getattr(llm_model, "model_name", None) != selected_model:
        logger.info("Initializing Groq model: %s", selected_model)
        llm_model = ChatGroq(model=selected_model, api_key=api_key, **kwargs)

    return llm_model


def invoke_model(prompt: str | list | Any, *, model_name: str | None = None, **kwargs):
    """Central place for all LLM calls in the project."""
    llm = get_llm(model_name=model_name, **kwargs)
    logger.info("Invoking LLM with model: %s", llm.model_name)
    return llm.invoke(prompt)


__all__ = ["invoke_model"]
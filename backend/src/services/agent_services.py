from core.logger import logger
from core.llm_model import invoke_model
from src.models.models import Agent
from src.models.schema import AgentConfig, AgentTitleUpdate, AgentConversationDelete

from sqlalchemy.orm import Session
from src.database import get_db

from fastapi import Depends, HTTPException
from core.config import setting




async def create_agent_conversation(
        db: Session = Depends(get_db),
        agent_config: AgentConfig = None) -> dict:

    prompt = agent_config.prompt

    try:
        llm_response = invoke_model(prompt, model_name=agent_config.model_name)

        if hasattr(llm_response, "content"):
            ai_response = llm_response.content
        else:
            ai_response = str(llm_response)

        new_agent = Agent(
            prompt = prompt,
            title = agent_config.title,
            role = agent_config.role,
            ai_response = ai_response,
            model_name = setting.model_name
        )

        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)

        logger.info("Agent conservation is created")

        return{
            "id":new_agent.id,
            "ai_response":new_agent.ai_response,
            "title":new_agent.title,
            "role":new_agent.role,
            "ai_response":new_agent.ai_response,
            "model_name" : new_agent.model_name,
        }
        
    except Exception as exc:
        logger.exception("Error creating agent conversation")
        raise ValueError(f"Failed to create agent conversation: {str(exc)}")





async def get_agent_conversation(db: Session = Depends(get_db)) -> list[dict]:
    conversation = db.query(Agent).order_by(Agent.created_at.desc())
    
    logger.info("Agent conservation is feteched")

    return [
        {
            "id": c.id,
            "title": c.title,
            "role": c.role,
            "prompt": c.prompt,
            "ai_response": c.ai_response,
            "model_name": c.model_name,
            "created_at": c.created_at.isoformat(),
        }
        for c in conversation
    ]


async def update_agent_conversation(
        conversation_id : int,
        title: AgentTitleUpdate,
        db:Session = Depends(get_db),) -> dict:

    conversation = db.query(Agent).filter(Agent.id == conversation_id).first()

    new_title = title.title.strip()

    if not new_title:
        raise HTTPException(status_code=400, detail="Updated title is needed")

    conversation.title = new_title
    db.commit()
    db.refresh(conversation)

    logger.info("Agent conservation is updated")

    return {
        "id": conversation.id,
        "title" : conversation.title
    }


def delete_agent_conversation(
        conversation_id: int,
        db : Session = Depends(get_db),
        ):

    conversation = db.query(Agent).filter(Agent.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=400, detail="Id isnot found")

    db.delete(conversation)
    db.commit()

    rows = db.query(Agent).order_by(Agent.id).all()

    for new_id, row in enumerate(rows, start=1):
        row.id = new_id
    db.commit()

    return {
        "message": "Conservation deleted sucessfully",
        "id" : conversation_id
    }


### -------------------------------Test Api-----------------------------------

async def agent(agent_config: AgentConfig):

    prompt = agent_config.prompt
    try:
        response = invoke_model(prompt)
        logger.info("Agent response: %s", response)
        return {"response": response}
    except Exception as e:
        logger.error("Error invoking model: %s", str(e))
        return {"error": str(e)}
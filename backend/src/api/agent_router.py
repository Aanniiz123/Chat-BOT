from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse


from sqlalchemy.orm import Session
from src.database import check_db_connection
from src.services.agent_services import (
    agent, 
    create_agent_conversation,
    get_agent_conversation,
    update_agent_conversation,
    delete_agent_conversation)

from src.database import get_db

router = APIRouter(prefix="/api/v1", tags=["Agent API"])


router.add_api_route("/agent", agent, methods=["GET"], status_code=status.HTTP_200_OK)


router.add_api_route("/create-conservation", create_agent_conversation, methods=["POST"], status_code=status.HTTP_200_OK)

router.add_api_route("/get-conservation", get_agent_conversation, methods=["GET"], status_code=status.HTTP_200_OK)

router.add_api_route("/update_agent_conversation", update_agent_conversation, methods=["PUT"], status_code=status.HTTP_200_OK)

router.add_api_route("/delete_agent_conversation/{conversation_id}", delete_agent_conversation, methods=["DELETE"], status_code=status.HTTP_200_OK)




@router.get("/health-check")
async def health_check():
    return {
        "status": "success",
        "message": "API is running successfully",
    }


@router.get("/db-health")
async def db_health_check():
    result = check_db_connection()
    if result["status"] == "success":
        return result
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=result)
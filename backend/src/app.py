from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.agent_router import router as agent_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(agent_router)


@app.get("/")
def health():
    return {"App is running"}


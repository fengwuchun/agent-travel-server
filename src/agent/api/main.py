
from fastapi import FastAPI
from agent.api.routes.travel import travel_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Al Travel Planner",version="0.1.0")
app.include_router(travel_router,prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

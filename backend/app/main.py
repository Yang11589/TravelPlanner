from fastapi import FastAPI
from app.api.planner import router 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




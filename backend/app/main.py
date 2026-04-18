from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.user import router as auth_router
from app.api.planner import router as planner_router

app = FastAPI()

# app.include_router(router, prefix="/api")
# app.include_router(router, prefix="/api/auth", tags=["auth"])
app.include_router(auth_router, prefix="/api")
app.include_router(planner_router, prefix="/api")

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




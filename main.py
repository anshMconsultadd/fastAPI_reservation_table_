from fastapi import FastAPI
from app.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(auth_router, tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin Routes"])
app.include_router(user_router, prefix="/user", tags=["User Routes"])


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routers import auth, knowledge, ranking, profile
from models.database import engine, Base
import os
from routers import comments
from dotenv import load_dotenv
load_dotenv()




app = FastAPI(title="Rebema API")

# CORS設定
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
app.include_router(ranking.router, prefix="/ranking", tags=["ranking"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(comments.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Rebema API"}

# ✅ Swagger UIでJWTを使えるようにするカスタムOpenAPI定義
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Rebema API",
        version="1.0.0",
        description="Rebema Backend API with JWT auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" not in method:
                method["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

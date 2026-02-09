from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.auth.router import router as auth_router
from app.menu.router import router as menu_router
from app.order.router import router as order_router
from app.table.router import router as table_router
from app.upload.router import router as upload_router

app = FastAPI(title="Table Order Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(menu_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(table_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

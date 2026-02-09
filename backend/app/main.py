from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
from app.core.config import settings
from app.auth.router import router as auth_router
from app.menu.router import router as menu_router
from app.order.router import router as order_router
from app.table.router import router as table_router
from app.upload.router import router as upload_router

class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        import json
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

app = FastAPI(
    title="Table Order Service", 
    version="1.0.0",
    default_response_class=UnicodeJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for static file serving
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(menu_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(table_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

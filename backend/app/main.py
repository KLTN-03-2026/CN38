from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers.auth import router as auth_router
from .routers.packages import router as packages_router
from .routers.users import router as users_router
from .routers.orders import router as orders_router
from .routers.payments import router as payments_router
from .routers.workouts import router as workouts_router
from .routers.ai import router as ai_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Hệ thống quản lý phòng gym tích hợp AI phân tích hành vi tập luyện",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(packages_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(orders_router, prefix=api_prefix)
app.include_router(payments_router, prefix=api_prefix)
app.include_router(workouts_router, prefix=api_prefix)
app.include_router(ai_router, prefix=api_prefix)


@app.get("/")
async def root():
    return {
        "message": "Gym Backend đang chạy",
        "status": "OK",
        "docs": "/docs",
        "api": api_prefix,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

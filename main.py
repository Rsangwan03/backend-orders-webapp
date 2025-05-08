from fastapi import FastAPI
from orders import router
from models import Base
from database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.middleware("http")
async def redirect_http_to_https(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(url))
    return await call_next(request)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins="https://stylestore-frontend-webapp-bpf4bjfgdha3gpcp.canadacentral-01.azurewebsites.net",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include orders router
app.include_router(router, prefix="/api", tags=["Orders"])

# Database setup on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

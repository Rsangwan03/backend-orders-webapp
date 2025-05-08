from fastapi import FastAPI, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

# 1. First - Handle Azure HTTPS redirects
@app.middleware("http")
async def azure_https_redirect(request: Request, call_next):
    if request.headers.get("x-forwarded-proto") == 'http':
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)

# 2. CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stylestore-frontend-webapp-bpf4bjfgdha3gpcp.canadacentral-01.azurewebsites.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 3. Explicit OPTIONS handler
@app.options("/api/orders")
async def options_handler():
    return {"Allow": "POST"}

# 4. Your existing routes
app.include_router(router, prefix="/api", tags=["Orders"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

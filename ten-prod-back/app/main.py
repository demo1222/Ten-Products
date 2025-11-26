from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, products, categories, cart, orders, courier, admin, farmer

app = FastAPI(title="Fresh Groceries Delivery API")

# Use a broad wildcard for origins to eliminate CORS as a cause for 'Failed to fetch' during development
# Note: allow_credentials must be False for wildcard origins in some configurations, but
# usually specific origins are safer. However, to debug connection issues, we'll add all local variants.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*" # Debug mode
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Explicit wildcard for debug
    allow_credentials=True, # Warning: this combo might be rejected by some browsers/proxies, but usually works for dev
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(courier.router)
app.include_router(admin.router)
app.include_router(farmer.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Fresh Groceries API"}

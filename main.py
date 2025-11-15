from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, products, orders, contact, admin
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kione Hardware API",
    description="Backend API for Kione Hardware Shop in Migori County",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(contact.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Kione Hardware API",
        "version": "1.0.0",
        "company": "Kione Hardware - Migori County",
        "ceo": "Viyl",
        "head_of_finance": "Ron"
    }
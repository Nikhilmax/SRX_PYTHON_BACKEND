from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import UserRead, AddressRead
from app.endpoints import users,products, orders
from app.db.session import get_db
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Welcome to the SRX API!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}    

@app.get("/info")
async def info():   
    return {
        "name": "SRX API",
        "description": "This is the SRX API for managing users and addresses.",
        "version": "1.0.0",
        "contact": {
            "name": "Nikhil Vecha",
            "email": "nikhilmax33@gmail.com"
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    }

app.include_router(users.router)

app.include_router(products.router)

app.include_router(orders.router)
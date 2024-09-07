from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, hospitals, staff, requests, donors, donations, repository
import models
from database import engine
from fastapi.middleware import Middleware

models.Base.metadata.create_all(bind=engine)


middleware = [
    Middleware(
        CORSMiddleware,
            allow_origins=["http://localhost:3000", "https://blood-bank-front.onrender.com"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

app = FastAPI(middleware=middleware)

app.include_router(auth.router)
app.include_router(hospitals.router)
app.include_router(staff.router)
app.include_router(requests.router)
app.include_router(donors.router)
app.include_router(donations.router)
app.include_router(repository.router)

@app.get("/")
async def root():
    return "Blood Bank System"

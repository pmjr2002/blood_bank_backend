from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, hospitals, staff, requests, donors, donations, repository
from . import models_
from app.database_ import engine

models_.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
    ".onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
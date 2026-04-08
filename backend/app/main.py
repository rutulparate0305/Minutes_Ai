from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Offline Meeting AI Backend Running"}
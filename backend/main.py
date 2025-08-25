from fastapi import FastAPI
from app.routers import expense
from app.db import engine
from app.models.expense import Base  # Make sure this import matches your project structure

app = FastAPI()
app.include_router(expense.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}

Base.metadata.create_all(bind=engine)
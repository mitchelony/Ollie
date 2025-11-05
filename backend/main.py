from email import message
from unicodedata import category
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# React Dev Server Request Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def root():
    return {"message": "Ollie backend running"}

@app.get("/api/expenses")
def get_expenses():
    return [
        {"category": "Food", "amount": 224.5},
        {"category": "Transport", "amount": 48.2},
        {"category": "Subscriptions", "amount": 19.99},
        {"category": "Supplies", "amount": 36.0},
        {"category": "Fun", "amount": 52.75},
    ]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth_router, transaction_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://expense-tracker-frontend-rose-theta.vercel.app",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",  # any local port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(transaction_router.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}
from fastapi import FastAPI
from routes import question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Speech Coach API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question.router)

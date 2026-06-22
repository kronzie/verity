from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI):
    """
    Attaches the CORS middleware bouncer to the FastAPI application.
    """
    # TODO 1: It's like a barrier for our application, it allows on whitelisted websites to read our resources, disallows malicious sites from accessing out private data, and allows only trusted websites to access or communicate with the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, this would be specific URLs like "https://my-streamlit-app.com"
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

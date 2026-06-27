from fastapi import FastAPI
from pydantic import BaseModel

# We import the setup function from your new modular folder!
from middlewares.cors import setup_cors
from middlewares.security import setup_security

print("Starting Verity API Gateway...")

# Initialize the FastAPI Waiter
app = FastAPI(title="Verity RAG API", version="1.0")

# --- MIDDLEWARE HALLWAY ---
# We call the function to attach the CORS bouncer
setup_cors(app)
setup_security(app)


# --- DATA VALIDATION (The Menu) ---
# TODO 2: Pydantic is great for data and schema  and very fast.
class QueryRequest(BaseModel):
    user_question: str
    security_clearance: str = "standard"


# --- REST ENDPOINTS (The Tables) ---

@app.get("/health")
def health_check():
    """A simple GET request to verify the server is alive."""
    return {"status": "200 OK", "message": "Verity API is running perfectly."}


# TODO 3: POST method is where the user sends something to backend, query is usually sent by user, if the backend reponds to the client then we can say the client server conection was successful.
@app.post("/query")
def process_query(request: QueryRequest):
    """
    Receives a question from the user, routes it through the RAG pipeline,
    and returns the AI's answer. (Pipeline logic coming soon!)
    """
    print(f"Intercepted query: {request.user_question} with clearance: {request.security_clearance}")

    # Fake response for now. We will connect Zone 3 here later!
    return {
        "status": "success",
        "question": request.user_question,
        "answer": "This is a placeholder answer from the kitchen."
    }

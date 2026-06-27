from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware bouncer that intercepts incoming requests to inspect the body
    for malicious prompt injection patterns before routing to endpoints.
    """
    async def dispatch(self, request: Request, call_next):
        # Only inspect POST requests targeting the query endpoint
        if request.method == "POST" and request.url.path == "/query":

            # 1. We read raw bytes because if a hacker sends corrupted data that isn't
            # valid JSON, trying to parse it as JSON immediately would crash our server.
            body_bytes = await request.body()
            body_str = body_bytes.decode("utf-8").lower()

            # Define heuristic attack signatures (Heuristic Validation)
            signatures = [
                "ignore previous instructions",
                "ignore past instructions",
                "clear your database",
                "print secret keys",
                "system prompt",
                "dan mode"
            ]

            # 2. String matching is instant and free. Using an LLM to check every message
            # would take seconds and cost money, allowing hackers to bankrupt us via spam.
            for signature in signatures:
                if signature in body_str:
                    print(f"ALERT: Security Middleware blocked an injection attempt matching signature: '{signature}'")
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Security Violation: Prompt Injection Detected"}
                    )

            # 3. Reading the request body empties the incoming data "stream". We must manually
            # refill it with our cached bytes so the actual endpoint has data to read later.
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            request._receive = receive

        # Pass the safe request down the hallway to the endpoint
        response = await call_next(request)
        return response

def setup_security(app: FastAPI):
    """Attaches the Security Middleware to the application instance."""
    app.add_middleware(SecurityMiddleware)

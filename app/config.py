import os

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))

RATE_LIMIT_LOGIN = int(os.getenv("RATE_LIMIT_LOGIN", "10"))  # per minute per IP

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


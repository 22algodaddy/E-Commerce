import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8001")
PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL",
    "http://payment-service:8003"
)


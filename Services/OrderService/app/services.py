import requests
from app.config import USER_SERVICE_URL, PRODUCT_SERVICE_URL
import requests
from app.config import USER_SERVICE_URL, PRODUCT_SERVICE_URL, PAYMENT_SERVICE_URL


def validate_user(user_id: str):
    response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if response.status_code != 200:
        raise Exception("User not valid")


def get_product(product_id: str):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code != 200:
        raise Exception("Product not found")
    return response.json()


def process_payment(order_id: str, amount: float):
    response = requests.post(
        f"{PAYMENT_SERVICE_URL}/pay",
        json={
            "order_id": order_id,
            "amount": amount
        },
        timeout=5
    )

    if response.status_code != 200:
        return "FAILED"

    return "PAID"

def validate_user(user_id: str):
    response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if response.status_code != 200:
        raise Exception("User not valid")

def get_product(product_id: str):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code != 200:
        raise Exception("Product not found")
    return response.json()



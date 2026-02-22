from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import random
import time

from app import schemas, metrics

app = FastAPI(title="Payment Service")


@app.post("/pay", response_model=schemas.PaymentResponse)
def process_payment(payment: schemas.PaymentRequest):
    metrics.PAYMENT_REQUEST_COUNT.inc()

    # Simulate processing delay
    time.sleep(1)

    # Simulate random failure (20% failure rate)
    if random.random() < 0.2:
        metrics.PAYMENT_FAILURE_COUNT.inc()
        raise HTTPException(status_code=400, detail="Payment failed")

    metrics.PAYMENT_SUCCESS_COUNT.inc()

    return {
        "order_id": payment.order_id,
        "status": "SUCCESS"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
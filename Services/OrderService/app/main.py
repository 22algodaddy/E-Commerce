from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, metrics, services
from app.database import engine, get_db
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

# Router with prefix
router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    metrics.ORDER_REQUEST_COUNT.inc()

    try:
        services.validate_user(order.user_id)
        product = services.get_product(order.product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 1: Create order as PENDING
    new_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        total_amount=product["price"],
        status="PENDING"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Step 2: Call payment service
    payment_status = services.process_payment(
        str(new_order.id),
        product["price"]
    )

    # Step 3: Update order status
    new_order.status = payment_status
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Attach router
app.include_router(router)
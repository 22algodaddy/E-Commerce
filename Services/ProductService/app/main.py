from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, metrics
from app.database import engine, get_db
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Service",
    docs_url="/products/docs",
    openapi_url="/products/openapi.json"
)


# Create router with prefix
router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    metrics.PRODUCT_REQUEST_COUNT.inc()

    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/", response_model=list[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    metrics.PRODUCT_REQUEST_COUNT.inc()
    return db.query(models.Product).all()


@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    metrics.PRODUCT_REQUEST_COUNT.inc()

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Include router
app.include_router(router)
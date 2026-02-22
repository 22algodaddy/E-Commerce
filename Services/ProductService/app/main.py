from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, metrics
from app.database import engine, get_db
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")


@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    metrics.PRODUCT_REQUEST_COUNT.inc()

    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products", response_model=list[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    metrics.PRODUCT_REQUEST_COUNT.inc()

    products = db.query(models.Product).all()
    return products


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    metrics.PRODUCT_REQUEST_COUNT.inc()

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


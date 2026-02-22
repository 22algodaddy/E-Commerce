from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth, metrics
from app.database import engine, get_db
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from app.auth import get_current_user
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    metrics.REQUEST_COUNT.inc()

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user or not auth.verify_password(
        form_data.password, db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/me", response_model=schemas.UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
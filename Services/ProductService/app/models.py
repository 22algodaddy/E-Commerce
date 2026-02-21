from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
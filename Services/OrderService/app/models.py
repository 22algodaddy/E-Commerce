from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    total_amount = Column(Float, nullable=False)
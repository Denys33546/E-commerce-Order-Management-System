from sqlalchemy import Column, Integer, String, Float, Text, JSON
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)  # Смартфоны, Ноутбуки и т.д.
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, default=0)
    specifications = Column(JSON, nullable=True)  # Окна характеристик (JSON)

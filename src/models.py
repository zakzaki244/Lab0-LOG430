
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
import datetime

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    products = relationship("Product", back_populates="store")


class Product(Base):
    __tablename__ = "products"
    id       = Column(Integer, primary_key=True)
    name     = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    price    = Column(Float)
    stock    = Column(Integer, default=0)
    store_id = Column(Integer, ForeignKey('stores.id'))   
    store = relationship("Store", back_populates="products")

class Sale(Base):
    __tablename__ = "sales"
    id        = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    items     = relationship("SaleItem", back_populates="sale", cascade="all, delete")

class SaleItem(Base):
    __tablename__ = "sale_items"
    id         = Column(Integer, primary_key=True)
    sale_id    = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity   = Column(Integer)
    sale       = relationship("Sale", back_populates="items")
    product    = relationship("Product")

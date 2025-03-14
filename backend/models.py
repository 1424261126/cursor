from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    company = Column(String(200))
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    orders = relationship("Order", back_populates="customer")
    tags = relationship("CustomerTag", back_populates="customer")
    messages = relationship("Message", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_name = Column(String(200))
    amount = Column(Float)
    status = Column(String(20))  # 待付款、已完成、已取消
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    customer = relationship("Customer", back_populates="orders")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CustomerTag(Base):
    __tablename__ = "customer_tags"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    tag_name = Column(String(50))
    is_auto_generated = Column(Boolean, default=False)
    
    # 关系
    customer = relationship("Customer", back_populates="tags")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    content = Column(Text)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    customer = relationship("Customer", back_populates="messages") 
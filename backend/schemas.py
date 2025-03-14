from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    company: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Order schemas
class OrderBase(BaseModel):
    product_name: str
    amount: float
    status: str

class OrderCreate(OrderBase):
    customer_id: int

class OrderUpdate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Tag schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# CustomerTag schemas
class CustomerTagBase(BaseModel):
    tag_name: str
    is_auto_generated: bool = False

class CustomerTagCreate(CustomerTagBase):
    customer_id: int

class CustomerTag(CustomerTagBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    is_ai_generated: bool = False

class MessageCreate(MessageBase):
    customer_id: int

class Message(MessageBase):
    id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True 
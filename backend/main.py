from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from ai_service import AIService

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="销售管理系统API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化AI服务
ai_service = AIService()

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 客户相关接口
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id=customer_id, customer=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

# 订单相关接口
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# 消息相关接口
@app.post("/messages/", response_model=schemas.Message)
async def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    # 创建客户消息
    db_message = crud.create_message(db=db, message=message)
    
    # 获取历史消息作为上下文
    history_messages = crud.get_customer_messages(db, customer_id=message.customer_id)
    context = [msg.content for msg in history_messages[-5:]]  # 只取最近5条消息
    
    # 生成AI回复
    ai_response = await ai_service.generate_response(message.content, context)
    
    # 创建AI回复消息
    ai_message = schemas.MessageCreate(
        customer_id=message.customer_id,
        content=ai_response,
        is_ai_generated=True
    )
    crud.create_message(db=db, message=ai_message)
    
    # 分析客户意图并添加标签
    tags = await ai_service.analyze_customer_intent(message.content)
    for tag in tags:
        crud.create_customer_tag(db=db, tag=schemas.CustomerTagCreate(
            customer_id=message.customer_id,
            tag_name=tag,
            is_auto_generated=True
        ))
    
    return db_message

@app.get("/messages/", response_model=list[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages

@app.get("/messages/{message_id}", response_model=schemas.Message)
def read_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.delete_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

# 标签相关接口
@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)

@app.get("/tags/", response_model=list[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.get_tags(db, skip=skip, limit=limit)
    return tags

@app.get("/tags/{tag_id}", response_model=schemas.Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.delete_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}

# 客户标签相关路由
@app.post("/customers/{customer_id}/tags/", response_model=schemas.CustomerTag)
def create_customer_tag(customer_id: int, tag: schemas.CustomerTagCreate, db: Session = Depends(get_db)):
    return crud.create_customer_tag(db=db, tag=tag)

@app.get("/customers/{customer_id}/tags/", response_model=list[schemas.CustomerTag])
def read_customer_tags(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_tags(db, customer_id=customer_id)

@app.delete("/customers/{customer_id}/tags/{tag_id}")
def delete_customer_tag(customer_id: int, tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.delete_customer_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}

@app.get("/customers/{customer_id}/messages/", response_model=list[schemas.Message])
def read_customer_messages(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_messages(db, customer_id=customer_id) 
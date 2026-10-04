import time
import socket
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database, rabbitmq


def wait_for_port(host: str, port: int, timeout: float = 30.0):
    """Блокирует запуск FastAPI, пока зависимая инфраструктура не поднимет порт"""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                break
        except socket.error:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Компонент инфраструктуры {host}:{port} не доступен.")
            time.sleep(1.0)


# Синхронизируем старт контейнера с фактической готовностью БД и Брокера
wait_for_port("postgres", 5432)
wait_for_port("rabbitmq", 5672)

# Создание базы данных и таблиц
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Service", version="1.0.0")


@app.post("/api/v1/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    db_order = models.Order(**order_data.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    event_data = {
        "order_id": db_order.id,
        "user_id": db_order.user_id,
        "product_id": db_order.product_id,
        "total_price": db_order.total_price,
        "status": db_order.status
    }

    # Публикация асинхронного события для Notification Worker
    rabbitmq.publish_order_event(event_type="order.created", data=event_data)
    return db_order


@app.get("/api/v1/orders", response_model=List[schemas.OrderResponse])
def read_orders(db: Session = Depends(database.get_db)):
    return db.query(models.Order).all()


@app.get("/api/v1/orders/{id}", response_model=schemas.OrderResponse)
def read_order(id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

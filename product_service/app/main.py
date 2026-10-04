import time
import socket
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, database
from .seed import seed_products  # ИСПРАВЛЕНО: Добавили импорт сид-скрипта!

def wait_for_port(host: str, port: int, timeout: float = 30.0):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                break
        except socket.error:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Сервис {host}:{port} не доступен.")
            time.sleep(1.0)

# Дожидаемся готовности PostgreSQL
wait_for_port("postgres", 5432)

# Создаем структуру таблиц
models.Base.metadata.create_all(bind=database.engine)

# ИСПРАВЛЕНО: Автоматически накатываем 50 товаров с характеристиками
seed_products()

app = FastAPI(title="Product Service", version="1.0.0")

@app.get("/api/v1/products", response_model=List[schemas.ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/api/v1/products/{id}", response_model=schemas.ProductResponse)
def read_product(id: int, db: Session = Depends(database.get_db)):
    product = crud.get_product(db, product_id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/v1/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db=db, product=product)

@app.put("/api/v1/products/{id}", response_model=schemas.ProductResponse)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    updated_product = crud.update_product(db=db, product_id=id, product_data=product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/api/v1/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(database.get_db)):
    if not crud.delete_product(db=db, product_id=id):
        raise HTTPException(status_code=404, detail="Product not found")
    return None
import time
import socket
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from . import models, schemas, crud, database
from .config import settings

def wait_for_port(host: str, port: int, timeout: float = 30.0):
    """Ожидает, пока порт инфраструктуры станет доступен внутри сети Docker"""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                break
        except socket.error:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Сервис {host}:{port} не ответил за {timeout} сек.")
            time.sleep(1.0)

# Гарантируем, что база данных готова принимать подключения
wait_for_port("postgres", 5432)

# Создание таблиц при старте
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="User Service", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) if not expires_delta else expires_delta
    to_encode.update({"exp": datetime.utcnow() + expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@app.post("/api/v1/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/v1/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/verify")
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "valid": True}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

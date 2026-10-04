#  E-Commerce Order Management System (Microservices Platform)

A production-style, event-driven microservices architecture built with **Python (FastAPI)**, **RabbitMQ**, **PostgreSQL**, and orchestrated via **Docker Compose** and **Nginx API Gateway**. It features an integrated, premium-styled **Telegram Bot Client** designed in the aesthetic of the Apple Store.

---

## 🏗️ Architecture Design

```text
                     ┌───────────────────┐
                     │    Telegram Bot   │ (Premium Storefront)
                     └─────────┬─────────┘
                               │ (Async HTTP)
                     ┌─────────▼─────────┐
                     │   Nginx Gateway   │ (API Entrypoint :8000)
                     └─────────┬─────────┘
                               │ (Reverse Proxy Load Balancing)
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
┌────────▼─────────┐  ┌────────▼─────────┐  ┌────────▼─────────┐
│   User Service   │  │ Product Service  │  │  Order Service   │
│   (Port 8001)    │  │   (Port 8002)    │  │   (Port 8003)    │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┤ (AMQP Async Event)
                               │                     │
                        ┌──────▼──────┐       ┌──────▼──────┐
                        │  PostgreSQL │       │   RabbitMQ  │
                        └─────────────┘       └──────┬──────┘
                                                     │ (order.created)
                                            ┌────────▼─────────┐
                                            │  Notification    │
                                            │     Worker       │
                                            └──────────────────┘
```

## 🛠️ Core Tech Stack & Demonstrated Skills

- **Backend Architecture:** Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic v2, JWT/OAuth2 Authentication.
- **Asynchronous Messaging:** RabbitMQ, Pub/Sub Pattern, Asymmetric Event Processing with `pika`.
- **DevOps & Infrastructure:** Docker containerization, Multi-Container Orchestration, Nginx API Gateway routing.
- **Database Engineering:** PostgreSQL isolation per service, JSON-based dynamic product specs schema.
- **Testing & Quality Assurance:** Automation test-suites with `pytest`, API integration tests using `httpx`.
- **CI/CD & Cloud:** GitHub Actions automated pipeline (Linting + Testing), ready-to-use **Kubernetes (K8s)** manifests.

---

## 🚀 Quick Start (Production-Like Orchestration)

Ensure you have **Docker Desktop** installed and running on your system.

### 1. Clone the project and configure the environment
```bash
git clone https://github.com
cd ecommerce-order-management
```

### 2. Launch the entire ecosystem with a single command
This will build all custom Python images, spin up isolated networks, and provision databases:
```bash
docker compose up -d --build
```

### 3. Verify that all 8 components are running smoothly
```bash
docker ps
```
*You should see 8 containers alive and kicking (Postgres, RabbitMQ, Nginx, 3 Services, Worker, and the Telegram Bot).*

### 4. Interactive API Documentation
Explore the gateway-routed endpoints via FastAPI automatic Swagger UI:
- **User Service Gate:** `http://localhost:8000/api/v1/auth/docs`
- **Product Catalog Gate:** `http://localhost:8000/api/v1/products`
- **Order Service Gate:** `http://localhost:8003/docs`

---

## 📊 End-to-End Event Scenario

1. **Premium Browsing:** A customer explores the dynamic tech catalog (pre-seeded with 50 diverse items) through the sleek Apple-styled Telegram Bot.
2. **Order Trigger:** Clicking **"🛍 Оформить заказ"** sends an async HTTP request to Nginx (`:8000`), routing it into `Order Service`.
3. **Database & Message Event:** `Order Service` commits the billing row to **PostgreSQL** and immediately fires an AMQP message `order.created` into **RabbitMQ**.
4. **Decoupled Job Execution:** The standalone `Notification Worker` instantly consumes the event from the broker queue, executing the checkout workflow concurrently without blocking the main thread.

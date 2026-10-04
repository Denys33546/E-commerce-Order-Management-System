import httpx
import os

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://nginx_gateway:8000")


class MockObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


async def set_user(tg_id: int):
    """Регистрация пользователя в user_service бэкенда"""
    async with httpx.AsyncClient() as client:
        try:
            payload = {"email": f"tg_{tg_id}@itshop.bot", "password": f"tg_pass_{tg_id}"}
            response = await client.post(f"{API_GATEWAY_URL}/api/v1/auth/register", json=payload, timeout=5.0)
            return response.status_code in [201, 400]
        except Exception as e:
            print(f"Ошибка регистрации: {e}")
            return False


async def get_categories():
    """ДИНАМИЧЕСКИЙ ВЫЗОВ: Получаем список уникальных категорий с бэкенда"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_GATEWAY_URL}/api/v1/products", timeout=5.0)
            if response.status_code == 200:
                products = response.json()
                # Извлекаем все уникальные названия категорий из списка товаров
                unique_categories = sorted(list(set(prod.get("category") for prod in products if prod.get("category"))))

                # Создаем список Mock-объектов с текстовым ID для клавиатуры aiogram
                return [MockObject(id=cat_name, name=cat_name) for cat_name in unique_categories]
            return []
        except Exception as e:
            print(f"Ошибка получения категорий: {e}")
            return []


async def get_items_by_category(category_name: str):
    """Получение списка товаров, отфильтрованных по названию категории"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_GATEWAY_URL}/api/v1/products", timeout=5.0)
            if response.status_code == 200:
                products = response.json()
                # Фильтруем товары по точному совпадению категории (например, "Ноутбуки")
                filtered = [prod for prod in products if prod.get("category") == category_name]
                return [MockObject(**prod) for prod in filtered]
            return []
        except Exception as e:
            print(f"Ошибка получения товаров по категории: {e}")
            return []


async def get_item(item_id):
    """Получение конкретного товара по его ID"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_GATEWAY_URL}/api/v1/products/{item_id}", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                return MockObject(**data)
            return None
        except Exception as e:
            print(f"Ошибка получения товара: {e}")
            return None


async def create_order_on_backend(tg_id: int, item_id: int, price: float):
    """Создание заказа в order_service через API Gateway"""
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "user_id": tg_id,
                "product_id": int(item_id),
                "quantity": 1,
                "total_price": float(price)
            }
            response = await client.post(f"{API_GATEWAY_URL}/api/v1/orders", json=payload, timeout=5.0)
            return response.status_code == 201, response.json()
        except Exception as e:
            print(f"Ошибка отправки заказа: {e}")
            return False, {}

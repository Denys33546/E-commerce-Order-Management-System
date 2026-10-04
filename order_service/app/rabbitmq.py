import pika
import json
from .config import settings  # Относительный импорт для работы внутри Docker

def publish_order_event(event_type: str, data: dict):
    try:
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Создаем устойчивую очередь для событий заказов
        channel.queue_declare(queue='order_events', durable=True)

        payload = {
            "event": event_type,
            "data": data
        }

        channel.basic_publish(
            exchange='',
            routing_key='order_events',
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Делаем сообщение персистентным
            )
        )
        print(f" [x] Sent event '{event_type}' with data: {data}")
        connection.close()
    except Exception as e:
        print(f" [!] Failed to publish event to RabbitMQ: {e}")

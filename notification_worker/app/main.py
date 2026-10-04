import pika
import json
import time
import sys
from config import settings  # Запуск идет из корня /app, импортируем без точки


def callback(ch, method, properties, body):
    try:
        # Декодируем полученное JSON-сообщение от RabbitMQ
        event_message = json.loads(body.decode())
        event_type = event_message.get("event")
        data = event_message.get("data")

        print(f" [▼] Received event: '{event_type}'")

        if event_type == "order.created":
            order_id = data.get("order_id")
            user_id = data.get("user_id")
            total_price = data.get("total_price")

            print(f" [→] Processing notification for Order #{order_id} (User: {user_id})")
            print(f" [→] Sending confirmation invoice for total: ${total_price}...")

            # Симулируем задержку отправки почтового/системного уведомления
            time.sleep(1)
            print(f" [✓] Notification for Order #{order_id} successfully processed!")

        # Подтверждаем RabbitMQ успешную обработку сообщения (удаляем из очереди)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("-" * 50)

    except Exception as e:
        print(f" [!] Error processing message: {e}")
        # В случае непредвиденного сбоя возвращаем задачу обратно в очередь
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_worker():
    print(" [*] Notification Worker is starting...")

    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )

    # Бесконечный цикл ожидания доступности сетевого сокета RabbitMQ при старте контейнеров
    for attempt in range(10):
        try:
            connection = pika.BlockingConnection(parameters)
            break
        except pika.exceptions.AMQPConnectionError:
            print(f" [!] RabbitMQ not ready yet. Retrying in 3 seconds... (Attempt {attempt + 1}/10)")
            time.sleep(3)
    else:
        print(" [!] Could not connect to RabbitMQ. Exiting.")
        sys.exit(1)

    channel = connection.channel()

    # Декларируем персистентную очередь
    channel.queue_declare(queue='order_events', durable=True)

    # Ограничиваем распределение: не давать воркеру больше 1 задачи одновременно
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='order_events', on_message_callback=callback)

    print(" [*] Waiting for order events. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()

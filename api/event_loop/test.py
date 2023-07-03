RABBIT_MQ_URL = "amqp://127.0.0.1:5672/"
import aiohttp
import asyncio
import aio_pika

async def process_message(message):
    print("Received:", message.body)
    # Дополнительная обработка сообщения

async def consume_messages():
    connection = await aio_pika.connect_robust(RABBIT_MQ_URL)
    routing_key = 'create_checker'
    channel = await connection.channel()
    queue = await channel.declare_queue(routing_key)

    

    print(await channel.default_exchange.publish(
        aio_pika.Message(body=f"Hello {routing_key}".encode()),
        routing_key=routing_key,
    ))

    await connection.close()


# Запуск асинхронного цикла событий
asyncio.run(consume_messages())
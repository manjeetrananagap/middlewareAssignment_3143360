import pika

def callback(ch, method, properties, body):
    print(f"Notification Service 1 received: {body}")

def consumeRabbitMQ():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # Declare the queue for order creation events
    channel.queue_declare(queue='OrderCreation_Only')

    # Set up callback for order creation events
    channel.basic_consume(queue='OrderCreation_Only', on_message_callback=callback, auto_ack=True)

    print('Notification Service 1 is waiting for order creation messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consumeRabbitMQ()

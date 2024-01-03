import pika

def callback(ch, method, properties, body):
    print(f"Notification Service 2 received : {body}")

def consumeRabbitMQ():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # Declare queues
    channel.queue_declare(queue='OrderCreation')
    channel.queue_declare(queue='OrderUpdating')

    # Set up callback for order creation events
    channel.basic_consume(queue='OrderCreation', on_message_callback=callback, auto_ack=True)

    # Set up callback for order updating events
    channel.basic_consume(queue='OrderUpdating', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consumeRabbitMQ()

from concurrent import futures
import grpc
import product_pb2
import product_pb2_grpc
from datetime import date
import pika

class PlaceOrderServiceServicer(product_pb2_grpc.PlaceOrderServiceServicer):
    def PlaceOrder(self, request, context):
        order = product_pb2.Order(
            order_id=request.product_id * 3,
            order_date=str(date.today()),
            product_id=request.product_id,
            msg="order placed successfully"
        )
        publishRabbitMQ(order)
        return order

    def UpdateOrder(self, request, context):
        # Implement the logic to update the order based on the UpdateOrderRequest
        updated_order = product_pb2.Order(
            order_id=request.order_id,
            order_date=str(date.today()),
            product_id=request.product_id,
            msg="order updated successfully"
        )
        publishRabbitMQ(updated_order)
        return updated_order

def publishRabbitMQ(order):
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    body = f"{order.msg}: Order Id is {order.order_id}"

    if order.msg == "order updated successfully":
        channel.basic_publish(exchange='', routing_key='OrderUpdating', body=f'OrderUpdating:{body}')
        channel.basic_publish(exchange='', routing_key='OrderCreation', body=f'OrderCreation:{body}')

    if order.msg == "order placed successfully":
        channel.basic_publish(exchange='', routing_key='OrderCreation_Only', body=body)


    connection.close()

if __name__ == '__main__':
    # Run a gRPC server with one thread.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    product_pb2_grpc.add_PlaceOrderServiceServicer_to_server(PlaceOrderServiceServicer(), server)
    server.add_insecure_port('[::]:6556')
    server.start()
    print('API server started. Listening at 127.0.0.1:6556.')
    server.wait_for_termination()

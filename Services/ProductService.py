
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import json
from functools import wraps
import datetime
from concurrent import futures
import codegen
import grpc 
import product_pb2
from product_pb2 import PlaceOrderRequest
import product_pb2_grpc

SERVER_ADDRESS = '127.0.0.1'
PORT = 6556


class ProductServiceClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{PORT}')
        self.stub = product_pb2_grpc.PlaceOrderServiceStub(self.channel)

    def get_placeOrder(self, product_id):
        request = product_pb2.PlaceOrderRequest(
            product_id=product_id
        )

        try:
            response = self.stub.PlaceOrder(request)
            print("gRPC response:", response)  # Add this line for debugging
            return response
        except grpc.RpcError as err:
            print("gRPC error details:", err.details())  # Add this line for debugging
            print('{}, {}'.format(err.code().name, err.code().value))  # Add this line for debugging
            return None

    def get_update_order(self, order_id, product_id):
        request = product_pb2.UpdateOrderRequest(order_id=order_id, product_id=product_id)
        try:
            response = self.stub.UpdateOrder(request)
            print("gRPC response:", response)  # Add this line for debugging
            return response
        except grpc.RpcError as err:
            print("gRPC error details:", err.details())  # Add this line for debugging
            print('{}, {}'.format(err.code().name, err.code().value))  # Add this line for debugging
            return None


products = [
	{
        'id': 100,
		'name': 'iPhone SE',
		'color': 'White',
        'description': 'Apple new launched.',
		'price': '100 rupee'
	},
	{
        'id': 200,
		'name': 'iPhone XR',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	},
    {
        'id': 300,
		'name': 'iPhone X',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	},
    {
        'id': 400,
		'name': 'iPhone 6',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	},
    {
        'id': 500,
		'name': 'iPhone 8',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	}
]

app = Flask(__name__)
client = ProductServiceClient()

#GET
@app.route('/') 
def print_hello():
	return 'Python gRPC'

@app.route('/products')
def get_products():
	return jsonify({'products': products})

@app.route('/productDetail/<int:id>')
def get_product_id(id):
    res = next((sub for sub in products if sub['id'] == id), None)
    return jsonify(res)	


@app.route('/placeOrder/<int:id>')
def place_order(id):
    res = client.get_placeOrder(id)
    if res is not None:
        return jsonify(
            {'product_id': res.product_id, 'order_id': res.order_id, 'order_date': res.order_date, 'Message': res.msg})
    else:
        return jsonify({'error': 'Failed to place order'}), 500  # Return an appropriate error response


@app.route('/updateOrder/<int:order_id>/<int:product_id>')
def update_order(order_id, product_id):
    res = client.get_update_order(order_id, product_id)

    if res is not None:
        return jsonify({'order_id': res.order_id, 'order_date': res.order_date, 'product_id': res.product_id})
    else:
        return jsonify({'error': 'Failed to update order'}), 500  # Return an appropriate error response

app.run(port=9000)


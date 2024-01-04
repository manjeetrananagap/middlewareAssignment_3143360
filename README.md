# middlewareAssignment_3143360

Language: Python
IDE: Pycharm

######  Import Services in IDE & flow mentioned steps to run the solution 

**Step 1** : run command to install the dependacy 

***pip3 install -r requirements.txt***

**Step 2** : Run python3 OrderService.py and ProductService.py to start gRPC in a separate terminals

**Step 3** : Start RabbitMQ service 

**Step 4** : Run python3 NotificationService2Consumer.py and NotificationService1Consumer.py in seprate terminals


**Note:** Solution build in windows OS 

**Assumption**
 
Created two Order Service using gRPC and consumed using Product service.
While order place from product service than product service call Order service using gRPC & return order id.
Same time Order service trigger notification msg of order id to rabbitMQ broker two services.


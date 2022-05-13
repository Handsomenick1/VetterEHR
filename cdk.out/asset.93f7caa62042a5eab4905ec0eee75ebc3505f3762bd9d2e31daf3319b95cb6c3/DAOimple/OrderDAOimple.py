import os
import boto3
import sys 
sys.path.append("..")
from DAO.OrderDAO import OrderDAO
from aws_helper.dynamoDB import update_item_db, scan_items_db, put_item_db

region = os.environ["region"]
order_table = os.environ["order_table"]
class OrderDAOimpl(OrderDAO):
   
    def __init__(self) -> None:
        self.orderTable = boto3.resource("dynamodb", region).Table(order_table)
        self.orders = {}
    #override
    def getAllOrders(self):
        self.orders = scan_items_db(self.orderTable)
        return self.orders

    #override
    def getOrder(self, OrderId):
        self.orders = scan_items_db(self.orderTable)
        for Order in self.orders:
            if Order.get("OrderId") == OrderId:
                return Order
        return None
    
    #override
    def updateOrder(self, OrderId, fileds: dict):
        try:
            for key in fileds:
                update_item_db(self.orderTable, "OrderId", OrderId, key, fileds.get(key))
            return True
        except Exception as e:
            return str(e)

    #override
    def deleteOrder(self, OrderId):
        pass
    
    # Override
    def addOrder(self, orderItem):
        put_item_db(self.orderTable, orderItem)
        return True

    def getOrderbycustomerId(self, customerId):
        self.orders = scan_items_db(self.orderTable)
        list = []
        for order in self.orders:
            if order.get("customerId") == customerId:
                list.append(order)
        if list:
            return list
        
        return None

    def getOrderbyclinicId(self, clinicId):
        self.orders = scan_items_db(self.orderTable)
        list = []
        for order in self.orders:
            if order.get("clinicId") == clinicId:
                list.append(order)
        if list:
            return list
        
        return None
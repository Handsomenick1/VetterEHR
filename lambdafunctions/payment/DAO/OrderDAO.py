import sys 
sys.path.append("..")
from abc import ABC, abstractmethod

class OrderDAO(ABC):
    @abstractmethod
    def getAllOrders(self):
        pass
    @abstractmethod
    def getOrder(self, orderId):
        pass
    @abstractmethod
    def updateOrder(self, orderId, filed: dict):
        pass
    @abstractmethod
    def deleteOrder(self, orderId):
        pass
    @abstractmethod
    def addOrder(self, orderItem):
        pass
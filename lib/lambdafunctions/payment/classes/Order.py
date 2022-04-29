import json
import sys 
import datetime
sys.path.append("..")

class Order:
    def __init__(self, listInfo) -> None:
        self.id = listInfo["id"]
        self.customerId = listInfo["customerId"]
        self.clinicId = listInfo["clinicId"]
        self.totalPrice = listInfo["totalPrice"]
        self.paymentURL = listInfo["paymentURL"]
        self.orderStatus = "uncomplete"
        self.paymentId = "UNKOWN"
        self.paymentStatus = False
        self.orderDate = str(datetime.datetime.now())
    
    def getId(self):
        return self.id
    def getclinicId(self):
        return self.clinicId
    def getcustomerId(self):
        return self.clinicId
    def gettotalprice(self):
        return self.totalPrice
    def getpaymenturl(self):
        return self.paymentURL
    def getpaymentstatus(self):
        return self.paymentStatus
    def getpaymentId(self):
        return self.paymentId
    def getorderstatus(self):
        return self.orderStatus
    def getorderdate(self):
        return self.orderDate
    def getOrderJSON(self):
        return json.dumps({
            "orderId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "totalPrice" : self.gettotalprice(),
            "paymentURL" : self.getpaymenturl(),
            "paymentStatus" : self.getpaymentstatus(),
            "paymentId" : self.getpaymentId(),
            "orderStatus" : self.getorderstatus(),
            "orderDate" : self.getorderdate()
        })
    
    def getOrderInfo(self):
        return {
            "orderId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "totalPrice" : self.gettotalprice(),
            "paymentURL" : self.getpaymenturl(),
            "paymentStatus" : self.getpaymentstatus(),
            "paymentId" : self.getpaymentId(),
            "orderStatus" : self.getorderstatus(),
            "orderDate" : self.getorderdate()
        }
    
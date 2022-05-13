import json
import sys 
sys.path.append("..")

class Order:
    def __init__(self, listInfo) -> None:
        self.id = listInfo["id"]
        self.customerId = listInfo["customerId"]
        self.clinicId = listInfo["clinicId"]
        self.totalPrice = listInfo["totalPrice"]
        self.paymentURL = listInfo["paymentURL"]
        self.paymentStatus = False
    
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
    
    def getOrderJSON(self):
        return json.dumps({
            "orderId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "totalPrice" : self.gettotalprice(),
            "paymentURL" : self.getpaymenturl(),
            "paymentStatus" : self.getpaymentstatus()
        })
    
    def getOrderInfo(self):
        return {
            "orderId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "totalPrice" : self.gettotalprice(),
            "paymentURL" : self.getpaymenturl(),
            "paymentStatus" : self.getpaymentstatus()
        }
    
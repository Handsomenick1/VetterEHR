import stripe
import logging
import decimal
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stripe.api_key = ""
from constants.Response import returnResponse
from DAOimple.OrderDAOimple import OrderDAOimpl
from classes.Order import Order
def lambda_handler(event, context):
    """
    {
    "body": {
        "userId": "customer001",
        "clinicId": "clinic001",
        "productInfo": [
        {
            "productName": "abc",
            "itemPrice": 100, (100 equals to $1.00)
            "itemQuantity": 1
        },
        {
            "productName": "def",
            "itemPrice": 100,
            "itemQuantity": 1
        }
        ]
    }
    }
    """
    logger.info("**** Start create payment service --->")
    orderDAOimpl = OrderDAOimpl()
    eventBody = event
    line_items = []
    i = 1
    totalprice = 0
    if type(event) == str:
        eventBody = event
    if "body" in eventBody:
        eventBody = eventBody["body"]
    else:
        return returnResponse(400, {"message": "Invalid input, no body"})

    if "productInfo" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no productInfo'})
    if "customerId" not in eventBody:
            return returnResponse(400, {'message': 'Invalid input, no customerId '})
    if "clinicId" not in eventBody:
            return returnResponse(400, {'message': 'Invalid input, no clinicId '})
         
    productList = eventBody["productInfo"]
    for product in productList:
        if "productName" not in product:
            return returnResponse(400, {'message': 'Invalid input, no productName in No{} product'.format(i)})
        if "itemPrice" not in product:
            return returnResponse(400, {'message': 'Invalid input, no itemPrice in No{} product'.format(i)})
        if "itemQuantity" not in product:
            return returnResponse(400, {'message': 'Invalid input, no itemQuantity in No{} product'.format(i)})
    
        productName = product["productName"]
        itemPrice = product["itemPrice"]
        itemQuantity = product["itemQuantity"]
        
        prooductResponse = stripe.Product.create(name=productName)
        logger.debug("**** No.{} prooductResponse ---> {}".format(i, prooductResponse))
        
        productId = prooductResponse.get("id")
        priceResponse = stripe.Price.create(
            unit_amount=itemPrice,
            currency="usd",
            product= productId,
        )
        logger.debug("**** No.{} priceResponse ---> {}".format(i, priceResponse))
        priceId = priceResponse.get("id")
        
        line_items.append({"price": priceId, "quantity": itemQuantity})
        i += 1
        totalprice += itemPrice / 100 * itemQuantity
    
    paymentResponse = stripe.PaymentLink.create(
        line_items = line_items,
         after_completion={
            "type": "redirect",
            "redirect": {"url": "https://development.d1wytw89nx1twe.amplifyapp.com"},
         }
    )
    logger.debug("**** paymentResponse ---> {}".format(paymentResponse))

    paymentURL = paymentResponse.get("url")
    
    orderId = paymentResponse.get("id")
    listInfo = {
        "id" : orderId, 
        "paymentURL" : paymentURL,
        "customerId" : eventBody["customerId"],
        "clinicId" : eventBody["clinicId"],
        "totalPrice" : decimal.Decimal(str(totalprice))
    }
    orderItem = Order(listInfo)
    orderobject = orderItem.getOrderInfo()
    orderDAOimpl.addOrder(orderobject)
    
    return returnResponse(200, {"url" : paymentURL, "orderId" : orderId})

import uuid
import stripe
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stripe.api_key = "sk_test_51KtbEeDSCRMRGAORSZXluw4EzrJOi9sVLZIziyk6ttPeNaiYlAxLlKSY6jYy28MrR83KOx2xL9mszFMQhb1hSdCK006fwnJzWv"
from constants.Response import returnResponse
from DAOimple.OrderDAOimple import OrderDAOimpl
from classes.Order import Order
def lambda_handler(event, context):
    # TODO implement
    logger.info("**** Start create payment service --->")
    orderDAOimpl = OrderDAOimpl()
    eventBody = event
    line_items = []
    i = 1
    totalprice = 0
    orderId = str(uuid.uuid4())
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
        line_items= line_items,
        after_completion={
            "hosted_confirmation": "Customer Paid",
            "custom_message" : "Thank you for your payment!!!"
        }
    )
    logger.debug("**** paymentResponse ---> {}".format(paymentResponse))

    paymentURL = paymentResponse.get("url")
    
    listInfo = {
        "id" : orderId, 
        "paymentURL" : paymentURL,
        "customerId" : eventBody["customerId"],
        "clinicId" : eventBody["clinicId"],
        "totalPrice" : totalprice
    }
    orderItem = Order(listInfo)
    orderobject = orderItem.getOrderInfo()
    orderDAOimpl.addOrder(orderobject)
    
    return returnResponse(200, {"url" : paymentURL})

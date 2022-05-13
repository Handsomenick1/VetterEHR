import os
import stripe
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stripe.api_key = "sk_test_51KtbEeDSCRMRGAORSZXluw4EzrJOi9sVLZIziyk6ttPeNaiYlAxLlKSY6jYy28MrR83KOx2xL9mszFMQhb1hSdCK006fwnJzWv"
from constants.Response import returnResponse
def lambda_handler(event, context):
    # TODO implement
    logger.info("**** Start create payment service --->")

    region = os.environ["region"]
    appointment_table = os.environ["appointment_table"]

    eventBody = event
    if type(event) == str:
        eventBody = event
    if "body" in eventBody:
        eventBody = eventBody["body"]
    else:
        return returnResponse(400, {"message": "Invalid input, no body"})

    if "productName" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no productName'})
    if "itemPrice" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no itemPrice'})
    if "itemQuantity" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no itemQuantity'})
    productList = eventBody["productInfo"]
    line_items = []
    i = 1
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
    
    paymentResponse = stripe.PaymentLink.create(
    line_items= line_items
    # Redirect to url after pay successfully
    # after_completion={
    #     "type": "redirect",
    #     "redirect": {"url": "https://example.com"},
    # },
    )
    logger.debug("**** paymentResponse ---> {}".format(paymentResponse))

    paymentURL = paymentResponse.get("url")
    
    returnResponse(200, {"url" : paymentURL})

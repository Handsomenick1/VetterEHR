import json
import os
import stripe
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stripe.api_key = "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"
from constants.Response import returnResponse
def lambda_handler(event, context):
    # TODO implement
    logger.info("**** Start set appointment service --->")

    region = os.environ["region"]
    appointment_table = os.environ["appointment_table"]
    appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)

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
    
    productName = eventBody["productName"]
    itemPrice = eventBody["itemPrice"]
    itemQuantity = eventBody["itemQuantity"]
    
    prooductResponse = stripe.Product.create(name=productName)
    logger.debug("**** prooductResponse ---> {}".format(prooductResponse))
    
    productId = prooductResponse.get("id")
    priceResponse = stripe.Price.create(
        unit_amount=itemPrice,
        currency="usd",
        recurring={"interval": "month"},
        product= productId,
    )
    logger.debug("**** priceResponse ---> {}".format(priceResponse))

    priceId = priceResponse.get("id")
    paymentResponse = stripe.PaymentLink.create(
    line_items=[{"price": priceId, "quantity": itemQuantity}],
    # after_completion={
    #     "type": "redirect",
    #     "redirect": {"url": "https://example.com"},
    # },
    )
    logger.debug("**** paymentResponse ---> {}".format(paymentResponse))

    paymentURL = paymentResponse.get("url")
    
    returnResponse(200, {"url" : paymentURL})

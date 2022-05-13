import sys 
sys.path.append("..")
import json
import logging
import stripe
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stripe.api_key = "sk_test_51KtbEeDSCRMRGAORSZXluw4EzrJOi9sVLZIziyk6ttPeNaiYlAxLlKSY6jYy28MrR83KOx2xL9mszFMQhb1hSdCK006fwnJzWv"

from constants.Response import returnResponse
from DAOimple.OrderDAOimple import OrderDAOimpl
def lambda_handler(event, context):
    # TODO implement
    logger.info("**** Start update payment service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    orderDAOimpl = OrderDAOimpl()
    
    eventBody = event
    
    orderId = eventBody["data"]["object"]["payment_link"]
    paymentId = eventBody["data"]["object"]["payment_intent"]
    orderStatus = eventBody["data"]["object"]["status"]
    fields = {"paymentStatus" : True, "paymentId" : paymentId, "orderStatus" : orderStatus}
    try:
        # deactive the payment
        stripe.PaymentLink.modify(
            orderId,
            active=False,
        )
        # update database
        orderDAOimpl.updateOrder(orderId, fields)
    except Exception as e:
        return returnResponse(400, str(e))
    return returnResponse(200, "Update paymentStatus successfully")

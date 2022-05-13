import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
from constants.Response import returnResponse
from DAOimple.OrderDAOimple import OrderDAOimpl
def lambda_handler(event, context):
    # TODO implement
    logger.info("**** Start update payment service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    orderDAOimpl = OrderDAOimpl()
    
    eventBody = event['queryStringParameters']
    
    if "orderId" not in eventBody:
        return returnResponse(400, {"message": "Invalid input, no orderId"})
    
    orderId = eventBody["orderId"]
    fields = {"paymentStatus" : True}
    try:
        orderDAOimpl.updateOrder(orderId, fields)
    except Exception as e:
        return returnResponse(400, str(e))
    return returnResponse(200, "Update paymentStatus successfully")

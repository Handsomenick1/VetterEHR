import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
from constants.Response import returnResponse
from DAOimple.OrderDAOimple import OrderDAOimpl
def lambda_handler(event, context):
    # TODO implement
    logger.info("**** Start get payment service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    orderDAOimpl = OrderDAOimpl()
    responseList = []    
    try:
       
        responseList = orderDAOimpl.getAllOrders()
        
        if responseList:
            return returnResponse(200, responseList)
        return returnResponse(400, "No data")
            
    except Exception as e:
        return returnResponse(400, str(e))
    
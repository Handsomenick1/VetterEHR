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
    responseList = []
    if "orderId" not in eventBody and "clinicId" not in eventBody and "customerId" not in eventBody and "doctorId" not in eventBody:
        return returnResponse(400, {"message": "Invalid input, no orderId/clinicId/customerId/doctorId"})
    
    try:
        if "orderId" in eventBody:
            orderId = eventBody['orderId']
            response = orderDAOimpl.getOrder(orderId)
            return returnResponse(200, response)
        if "customerId" in eventBody:
            customerId = eventBody['customerId']
            responseList = orderDAOimpl.getAllOrders(customerId)
        if "clinicId" in eventBody:
            clinicId = eventBody['clinicId']
            responseList = orderDAOimpl.getAllOrders(clinicId)
        
        if responseList:
            return returnResponse(200, responseList)
        return returnResponse(400, "No data")
            
    except Exception as e:
        return returnResponse(400, str(e))
    
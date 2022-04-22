import json
import logging
import boto3
import os
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
from constants.Response import returnResponse
from constants.NoItemError import NoitemError
from aws_helper.dynamoDB import put_item_db, get_item_db, get_items_db, update_item_db

region = os.environ["region"]
appointment_table = os.environ["appointment_table"]
appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)

def lambda_handler(event, context):
    """
    appointmentId, clinicId, customerId, doctorId
    """
    logger.info("**** Start retrieve appointment Info service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    eventBody = event['queryStringParameters']

    if "appointmentId" not in eventBody and "clinicId" not in eventBody and "customerId" not in eventBody and "doctorId" not in eventBody:
        return returnResponse(400, {"message": "Invalid input, no appointmentId/clinicId/customerId/doctorId"})
    
    response_list = []
    try:
        if "appointmentId" in eventBody:
            response = get_item_db(appointmentTable, "appointmentId", eventBody["appointmentId"])
            return returnResponse(200, response)

        if "clinicId" in eventBody:
            response_list = get_items_db(appointmentTable, "clinicId", eventBody["clinicId"])
        
        if "customerId" in eventBody:
            response_list = get_items_db(appointmentTable, "customerId", eventBody["customerId"])
        
        if "doctorId" in eventBody:
            response_list = get_items_db(appointmentTable, "doctorId", eventBody["doctorId"])
        
        return returnResponse(200, response_list)
        
    except NoitemError as ne:
        return returnResponse(400, str(ne))
    
    except Exception as e:
        return returnResponse(400, str(e))


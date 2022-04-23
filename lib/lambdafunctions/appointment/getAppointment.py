import json
import logging
import boto3
import os

from appointment.constants.Response import returnResponse
from appointment.constants.NoItemError import NoitemError
from appointment.aws_helper.dynamoDB import put_item_db, get_item_db, get_items_db, update_item_db

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    """
    appointmentId, clinicId, customerId, doctorId
    """
    logger.info("**** Start retrieve appointment Info service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    region = os.environ["region"]
    appointment_table = os.environ["appointment_table"]
    appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)

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
        
        if response_list: 
            return returnResponse(200, response_list)

        return returnResponse(204, "No data")

    except NoitemError as ne:
        return returnResponse(400, str(ne))
    
    except Exception as e:
        return returnResponse(400, str(e))


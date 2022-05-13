import json
import logging
import boto3
import os
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import sys 
sys.path.append("..")
from appointment.constants.Response import returnResponse
from appointment.aws_helper.dynamoDB import put_item_db, get_item_db, get_items_db, update_item_db
from appointment.constants.AppointmentStatus import AppointmentStatus


def lambda_handler(event, context):
    logger.info("**** Start confirm service --->")
    logger.debug('event:{}'.format(json.dumps(event)))

    region = os.environ["region"]
    appointment_table = os.environ["appointment_table"]
    appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)

    eventBody = event
    if type(event) == str:
        eventBody = event
    if "body" in eventBody:
        eventBody = eventBody["body"]
    else:
        return returnResponse(400, {"message": "Invalid input, no queryStringParameters"})
    
    if "appointmentId" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no appointmentId'})

    appointmentId = eventBody["appointmentId"]

    # Update status to CONFIRMED
    try:
        update_item_db(appointmentTable, "appointmentId", appointmentId, "appointmentStatus", AppointmentStatus.CONFIRM.value)
    except Exception as e:
        logger.debug(str(e))
        return returnResponse(400, "Someting worng with confirm_handler()")
    
    return returnResponse(200, "update to confrim succeeded")
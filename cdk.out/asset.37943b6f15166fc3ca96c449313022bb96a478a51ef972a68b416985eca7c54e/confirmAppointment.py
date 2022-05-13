import json
import logging
import boto3
import os
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import sys 
sys.path.append("..") 
from constants.Response import returnResponse
from aws_helper.dynamoDB import update_item_db
from constants.AppointmentStatus import AppointmentStatus


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
        return returnResponse(400, {"message": "Invalid input, no `body` in the request"})
    
    if "appointmentId" in eventBody:
        appointmentId = eventBody["appointmentId"]
        try:
            update_item_db(appointmentTable, "appointmentId", appointmentId, "appointmentStatus", AppointmentStatus.CONFIRM.value)
            return returnResponse(200, "appointment update to confrimed succeeded")
        except Exception as e:
            logger.debug(str(e))
        return returnResponse(400, "Someting worng with confirm_handler()")

    if "docterId" in eventBody:
        docterId = eventBody["docterId"]
        try:
            update_item_db(appointmentTable, "appointmentId", appointmentId, "docterId", docterId)
            return returnResponse(200, "appointment update to confrimed succeeded")
        except Exception as e:
            logger.debug(str(e))
        return returnResponse(400, "Someting worng with confirm_handler()")
    
    return returnResponse(400, {"message": "Missing `appointmentId` or `docterId` in the reqeust" })
    

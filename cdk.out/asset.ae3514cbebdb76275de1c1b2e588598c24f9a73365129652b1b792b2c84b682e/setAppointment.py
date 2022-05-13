import os
import boto3
import logging
import sys 
sys.path.append("..") 
from classes.Appointment import Appointment
from constants.Response import returnResponse
from aws_helper.dynamoDB import put_item_db

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    """
    {
        "body": {
            "appointmentId": "",
            "customerId": "",
            "clinicId": "",
            "appointmentDate": "",
            "reason": ""
        }
    }
    """
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

    if "appointmentId" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no appointmentId'})
    if "userId" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no userId'})
    if "clinicId" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no clinicId'})
    if "appointmentDate" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no appointmentDate'})
    if "reason" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no reason'})

    appointmentObj = Appointment(eventBody)
    appointmentItem = appointmentObj.getAppointmentInfo()

    try:
        put_item_db(appointmentTable, appointmentItem)
        return returnResponse(200, "Create {} appointment succeeded".format(eventBody["appointmentId"]))
    except Exception as e:
        return returnResponse(400, str(e))

import imp
import os
import json
import boto3
import logging
import decimal

from classes.Appointment import Appointment
from aws_helper.dynamoDB import put_item_db, get_item_db, get_items_db, update_item_db

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dynamodb_client = boto3.client('dynamodb')
region = os.environ["region"]
appointment_table = os.environ["appointment_table"]
appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)

def lambda_handler(event, context):
    """
    customerId, clinicId, Date, Reason
    """
    logger.info("**** Start set appointment service --->")

    eventBody = event
    if type(event) == str:
        eventBody = event
    if "body" in eventBody:
        eventBody = eventBody["body"]
    else:
        return returnResponse(400, {"message": "Invalid input, no body"})

    if "appointmentId" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no appointmentId'})
    if "customerId" not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no customerId'})
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
        return returnResponse(200, "Create {} appointment succeesded".format(eventBody["appointmentId"]))
    except Exception as e:
        return returnResponse(400, str(e))

def returnResponse(statusCode, body):
    logger.debug("[RESPONSE] statusCode: {} body: {}".format(statusCode, body))
    logger.debug("[RESPONSE] json.dumps(body): {}".format(json.dumps(body, indent=4, cls=DecimalEncoder)))
    return {
        "statusCode": statusCode,
        "body": json.dumps(body, indent=4, cls=DecimalEncoder),
        "isBase64Encoded": False,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Credentials": True,
            "Content-Type": "application/json"
        }
    }

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
import json
import logging
import boto3
import os
import sys 
sys.path.append("..") 
from constants.Response import returnResponse
from constants.NoItemError import NoitemError
from aws_helper.dynamoDB import scan_items_db

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info("**** Start retrieve all appointments Info service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    region = os.environ["region"]
    appointment_table = os.environ["appointment_table"]
    appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)

    response_list = []
    try:
        response_list = scan_items_db(appointmentTable)
        
        if response_list: 
            return returnResponse(200, response_list)

        return returnResponse(204, "No data")

    except NoitemError as ne:
        return returnResponse(400, str(ne))
    
    except Exception as e:
        return returnResponse(400, str(e))


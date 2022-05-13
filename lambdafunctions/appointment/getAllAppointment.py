import json
import logging
import boto3
import os
import sys 
sys.path.append("..") 
from constants.Response import returnResponse
from constants.NoItemError import NoitemError
from aws_helper.dynamoDB import scan_items_db
from DAOimpl.AppointmentDAOimpl import AppointmentDAO
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info("**** Start retrieve all appointments Info service --->")
    
    appointmentDAO = AppointmentDAO()
    response_list = []
    try:
        response_list = appointmentDAO.getAllappointments()
        if response_list: 
            return returnResponse(200, response_list)

        return returnResponse(204, "No data")

    except NoitemError as ne:
        return returnResponse(400, str(ne))
    
    except Exception as e:
        return returnResponse(400, str(e))


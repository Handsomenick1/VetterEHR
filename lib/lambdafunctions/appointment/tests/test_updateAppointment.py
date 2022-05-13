import sys 
sys.path.append("..")
from lib.lambdafunctions.appointment.updateAppointment import lambda_handler
from lib.lambdafunctions.appointment.aws_helper.dynamoDB import put_item_db, get_item_db
from lib.lambdafunctions.appointment.constants.AppointmentStatus import AppointmentStatus
import pytest
import unittest
import boto3
from moto import mock_dynamodb2

@mock_dynamodb2
class test_updateAppointment(unittest.TestCase):
    
    def test_updateAppointment_happy(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_table'
        table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'appointmentId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'appointmentId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        data = {
                    
                    'appointmentId':'appointmenttest',
                    'userId':'customertest',
                    'clinicId': 'clinictest',
                    'appointmentDate' : '07/08/2022',
                    "appointmentStatus" :AppointmentStatus.UNCONFIRM.value,
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)

        event = {
            "body" : {
                "appointmentId" : "appointmenttest",
                "appointmentDate" : "09/22/2023",
                "reason" : "vaccine"
                
            }
        }                
        response = lambda_handler(event, '')
        result = get_item_db(table, "appointmentId", "appointmenttest")
        assert response["statusCode"] == 200
        assert result["appointmentDate"] == "09/22/2023"
        assert result["reason"] == "vaccine"
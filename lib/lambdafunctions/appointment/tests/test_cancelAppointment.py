
import sys 
sys.path.append("..")
from lib.lambdafunctions.appointment.cancelAppointment import lambda_handler
from lib.lambdafunctions.appointment.aws_helper.dynamoDB import put_item_db, get_item_db
from lib.lambdafunctions.appointment.constants.AppointmentStatus import AppointmentStatus
import pytest
import unittest
import boto3
from moto import mock_dynamodb2

@mock_dynamodb2
class test_cancelAppointment(unittest.TestCase):
    
    def test_cancelAppointment_happy(self):
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
                    'customerId':'customertest',
                    'clinicId': 'clinictest',
                    'appointmentDate' : '07/08/2022',
                    "appointmentStatus" :AppointmentStatus.UNCONFIRM.value,
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)

        event = {
            "body" : {
                "appointmentId" : "appointmenttest"
            }
        }                
        response = lambda_handler(event, '')
        result = get_item_db(table, "appointmentId", "appointmenttest")
        assert response["statusCode"] == 200
        assert result["appointmentStatus"] == AppointmentStatus.CANCEL.value
    
    def test_cancelAppointment_failed(self):
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
                    'customerId':'customertest',
                    'clinicId': 'clinictest',
                    'appointmentDate' : '07/08/2022',
                    "appointmentStatus" :AppointmentStatus.UNCONFIRM.value,
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        
        event = {
            "body" : {
                
            }
        }                
        response = lambda_handler(event, '')
        assert response["statusCode"] == 400

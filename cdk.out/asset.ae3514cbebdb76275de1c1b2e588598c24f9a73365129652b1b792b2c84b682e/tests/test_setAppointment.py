
from lib.lambdafunctions.appointment.setAppointment import lambda_handler
import pytest
import unittest
import boto3
from moto import mock_dynamodb2

@mock_dynamodb2
class test_setAppointment(unittest.TestCase):
    
    def test_setAppointment_happy(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_table'
        table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'appointmentId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'appointmentId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        event = {
                    'body': {
                        'appointmentId':'appointmenttest',
                        'userId':'customertest',
                        'clinicId': 'clinictest',
                        'appointmentDate' : '07/08/2022',
                        'reason': 'Sick'
                        }
                }
                        
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 200

    def test_setAppointment_table_failed(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_table'
        
        event = {
                    'body': {
                        'appointmentId':'appointmenttest',
                        'userId':'customertest',
                        'clinicId': 'clinictest',
                        'appointmentDate' : '07/08/2022',
                        'reason': 'Sick'
                        }
                }
                        
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 400

    def test_setAppointment_fileds_failed(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_table'
        table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'appointmentId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'appointmentId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        event = {
                    'body': {
                        'appointmentId':'appointmenttest',
                        'clinicId': 'clinictest',
                        'appointmentDate' : '07/08/2022',
                        'reason': 'Sick'
                        }
                }
                        
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 400
    
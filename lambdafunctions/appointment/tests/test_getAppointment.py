
import sys 
sys.path.append("..")
from lambdafunctions.appointment.getAppointment import lambda_handler
from lambdafunctions.appointment.aws_helper.dynamoDB import put_item_db
import pytest
import unittest
import boto3
from moto import mock_dynamodb2

@mock_dynamodb2
class test_getAppointment(unittest.TestCase):
    
    def test_getAppointment_appointmentId_happy(self):
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
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        event = {
            "queryStringParameters" : {
                "appointmentId" : "appointmenttest"
            }
        }                
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 200

    def test_getAppointment_customerId_happy(self):
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
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        event = {
            "queryStringParameters" : {
                "userId" : "customertest"
            }
        }                
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 200

    def test_getAppointment_clinicId_happy(self):
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
                    'doctorId': 'doctortest',
                    'appointmentDate' : '07/08/2022',
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        event = {
            "queryStringParameters" : {
                "clinicId" : "clinictest"
            }
        }                
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 200
    
    def test_getAppointment_doctorId_happy(self):
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
                    'doctorId': 'doctortest',
                    'appointmentDate' : '07/08/2022',
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        event = {
            "queryStringParameters" : {
                "doctorId" : "doctortest"
            }
        }                
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 200
    
    def test_getAppointment_appointmentId_failed(self):
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
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        event = {
            "queryStringParameters" : {
                "appointmentId" : "appointmenttest1"
            }
        }                
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 400
    
    def test_getAppointment_listInfo_failed(self):
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
                    'reason': 'Sick'
                        
                }
        put_item_db(table, data)
        event = {
            "queryStringParameters" : {
                "userId" : "appointmenttest1"
            }
        }                
        response = lambda_handler(event, '')
        
        assert response["statusCode"] == 204
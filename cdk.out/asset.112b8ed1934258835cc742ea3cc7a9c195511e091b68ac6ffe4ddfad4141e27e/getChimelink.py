
import boto3
from constants.Response import returnResponse
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('chime')
    try:
        response = client.create_meeting(
            MediaRegion='us-west-2',
            
        )
        logger.debug('response -------> {}'.format(response))

        return returnResponse(200, response)
    
    except Exception as e:
        logger.debug('event:{}'.format(str(e)))
        return returnResponse(400, str(e))
    

    


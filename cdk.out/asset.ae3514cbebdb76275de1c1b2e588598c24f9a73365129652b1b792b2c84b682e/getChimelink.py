
import boto3
from constants.Response import returnResponse
import json
import uuid
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('chime')
    ExternalUserId1 = str(uuid.uuid4())
    ExternalUserId2 = str(uuid.uuid4())
    try:
        meetingResponse = client.create_meeting_with_attendees(
            MediaRegion='us-west-2',
            Attendees=[
                {
                    'ExternalUserId': ExternalUserId1,
                },
                {
                    'ExternalUserId': ExternalUserId2,
                },
                
            ]
            
        )
        logger.debug('meetingResponse -------> {}'.format(meetingResponse))


        return returnResponse(200, meetingResponse)
    
    except Exception as e:
        logger.debug('event:{}'.format(str(e)))
        return returnResponse(400, str(e))
    

    


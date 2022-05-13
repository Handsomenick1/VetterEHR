import jwt
import requests
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
from time import time
from constants.Response import returnResponse

# Enter your API key and your API secret
API_KEY = 'eKzH8tmySViAi29U5WD_JA'
API_SEC = 'FKLOygY0h00Tsr9SI0Z0jxVe00ke6SOJQGpf'

# create a function to generate a token
# using the pyjwt library

def lambda_handler(event, context):
    logger.info("**** Start genarate zoom meeting service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    eventBody = event
    if type(event) == str:
        eventBody = event
    if "body" in eventBody:
        eventBody = eventBody["body"]
    else:
        return returnResponse(400, {"message": "Invalid input, no `body` in the request"})
    if "startTime" not in eventBody:
        return returnResponse(400, {"message": "Invalid input, no `startTime` in the body"})

    # parse event
    startTime = eventBody["startTime"]
    # generateToken
    token = generateToken()
    # generate meetingdetails
    meetingdetails = getmeetingdetails(startTime)
    # pass token and meetingdetails to createMeeting
    meetingInfo = createMeeting(meetingdetails, token)
    print(meetingInfo)
    return returnResponse(200, meetingInfo)

def generateToken():
	myToken = jwt.encode(
		# Create a payload of the token containing
		# API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},API_SEC,algorithm='HS256'
	)
	return myToken

def createMeeting(meetingdetails, token):
    headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    r = requests.post(
		f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails)
        )
    y = json.loads(r.text)
    url = y["join_url"]
    password = y["password"]
    meetingInfo = {
        "url" : url,
        "password" : password
    }
    return meetingInfo
	
    
# create json data for post requests
def getmeetingdetails(startTime):
    meetingdetails = {"topic": "Online vetter",
                "type": 2,
                "start_time": "".format(startTime), # 2019-06-14T10: 21: 57
                "duration": "45",
                "timezone": "Europe/Madrid",
                "agenda": "test",

                "recurrence": {"type": 1,
                                "repeat_interval": 1
                                },
                "settings": {"host_video": "true",
                            "participant_video": "true",
                            "join_before_host": "False",
                            "mute_upon_entry": "False",
                            "watermark": "true",
                            "audio": "voip",
                            "auto_recording": "cloud"
                            }
                }
    return meetingdetails


# event = {
#     "body" : {
#         "startTime" : "2022-06-14T10: 21: 57"
#     }
# }

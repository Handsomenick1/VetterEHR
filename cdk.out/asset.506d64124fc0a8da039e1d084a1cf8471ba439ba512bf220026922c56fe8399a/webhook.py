import json
import datetime

import stripe
import boto3
import logging
# from aws_xray_sdk.core import patch_all
# from aws_xray_sdk.core import xray_recorder

STRIPE_SIGNATURE_HEADER = "Stripe-Signature"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
stripe.api_key = "sk_test_51KtbEeDSCRMRGAORSZXluw4EzrJOi9sVLZIziyk6ttPeNaiYlAxLlKSY6jYy28MrR83KOx2xL9mszFMQhb1hSdCK006fwnJzWv"

# Logger can be reused
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Instrument libraries for AWS XRay
# patch_all()
eventbridge_client = boto3.client("events")
stripe_signing_secret = 'whsec_4f0e4d01d0c9f0d17894c67ef763c1739a4167c1795e16c83f04b1a855263f93'

def lambda_handler(event, context):
    logger.debug(f"Lambda event: {json.dumps(event)}")
    type = event["type"]
    eventbridge_client.put_events(
        Entries=[
            {
                "Time": datetime.datetime.now(),
                "Source": "stripe",
                "DetailType": type,
                "Detail": json.dumps(event),
            }
        ]
    )

    return {"statusCode": 200, "done" : True}
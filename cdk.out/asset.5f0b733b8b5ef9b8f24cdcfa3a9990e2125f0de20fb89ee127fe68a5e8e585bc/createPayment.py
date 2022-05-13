import json
import stripe
stripe.api_key = "sk_test_51KtbEeDSCRMRGAORSZXluw4EzrJOi9sVLZIziyk6ttPeNaiYlAxLlKSY6jYy28MrR83KOx2xL9mszFMQhb1hSdCK006fwnJzWv"

def lambda_handler(event, context):
    # TODO implement
    preoductResponse = stripe.Product.create(name="Gold Special")
    productId = preoductResponse.get("id")
    priceResponse = stripe.Price.create(
        unit_amount=5000000,
        currency="usd",
        recurring={"interval": "month"},
        product= productId,
    )
    return {
        'statusCode': 200,
        'body': json.dumps(priceResponse)
    }

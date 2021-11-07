import requests
import json
import math
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
# NLU stuff
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


def get_request(url, api_key = None, **kwargs):
    print(kwargs)
    try:
        if api_key is not None and len(api_key) > 0:
            print("GET from {} with AUTH".format(url))
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('api_key', api_key))
        else:
            print("GET from {} ".format(url))    
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs 
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    try:
        print("POST from {} ".format(url))    
        response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    except:
        # If any error occurs 
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def _get_dealers_from_cf_by_url(url):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer in dealers:
            # print(f"dealer={dealer}")
            results.append(CarDealer.create(dealer))
    return results

def get_dealers_from_cf():
    return _get_dealers_from_cf_by_url("https://9cecc68d.us-south.apigw.appdomain.cloud/api/dealership")

def get_dealer_by_id_from_cf(dealer_id):
    return _get_dealers_from_cf_by_url(f"https://9cecc68d.us-south.apigw.appdomain.cloud/api/dealership?dealer_id={dealer_id}")

def get_dealers_by_state_from_cf(state):
    return _get_dealers_from_cf_by_url(f"https://9cecc68d.us-south.apigw.appdomain.cloud/api/dealership?state={state}")

def get_dealer_reviews_from_cf(dealerId):
    results = []
    json_result = get_request(f"https://9cecc68d.us-south.apigw.appdomain.cloud/api/review/?dealerId={dealerId}")
    if json_result and "body" in json_result:
        reviews = json_result["body"]
        # print(reviews)
        for review in reviews:
            review['sentiment'] = analyze_review_sentiments(review['review'])
            # print(f"review={review}")
            results.append(DealerReview.create(review))
    return results

def analyze_review_sentiments(text):
    # Note: I'm going to follow IBM NLU API instead because Course Lab example doesn't work.
    NLU_API_KEY = 'DXuXmEdb4oO8_cYAVYzWJWd2X5gr6EmR_uwwkK8nNDyO'
    NLU_API_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/11e325c0-baff-4704-bcc0-3cbc7df478c4'
    sentiment = "neutral"

    authenticator = IAMAuthenticator(NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
        )

    natural_language_understanding.set_service_url(NLU_API_URL)

    print(f"Analyzing sentiment for: {text}")
    try:
        word_count = math.ceil(len(text.split()) / 2)
        if word_count <= 0:
            word_count = 1
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                keywords=KeywordsOptions(emotion=False, sentiment=True, limit=word_count)
                )
            ).get_result()
        if "keywords" in response:
            keywords = response['keywords']
            sentiment_tally = {
                "positive" : 0,
                "negative" : 0,
                "neutral" : 0
                }
            highest = "neutral"
            for keyword in keywords:
                key = keyword['sentiment']['label']
                sentiment_tally[key] += 1
                if sentiment_tally[key] > sentiment_tally[highest]:
                    highest = key
            sentiment = highest
        print(json.dumps(response, indent=2))
    except ApiException as ae:
        print("NLU ApiException: {}".format(ae))
    print(f"Final sentiment: {sentiment}")
    return sentiment

def add_review_to_cf(json_payload):
    results = []
    url = "https://9cecc68d.us-south.apigw.appdomain.cloud/api/review"
    json_result = post_request(url, json_payload=json_payload)
    print(f"json_result={json_result}")
    if json_result and "body" in json_result:
        reviewId = json_result["body"]
        print(f"reviewId={reviewId}")
        results.append({
            "reviewId" : reviewId
            })
    return results


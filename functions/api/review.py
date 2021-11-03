#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
import json

def http_error(status_code, message):
    return {
        "headers" : { "Content-Type" : "application/json" },
        "statusCode" : status_code,
        "code": status_code,
        "error": message
        }

def main(dict):
    COUCH_USERNAME = "0886bfd5-cf1b-4e75-b0bb-e21190990f4f-bluemix"
    IAM_API_KEY = "P4ML4YSIiBDR3uJoMw_7ymwT_XUSFI5Ikyd_W4fKr52-"
    databaseName = "reviews"

    try:
        client = Cloudant.iam(
            account_name=COUCH_USERNAME,
            api_key=IAM_API_KEY,
            connect=True,
            )
        db = client[databaseName]
    except CloudantException as ce:
        print("unable to connect")
        return http_error(500, ce)
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return http_error(500, err)

    # GET
    if "dealerId" not in dict or dict["dealerId"] is None:
        print("dealerId does not exist.")
        return http_error(404, "dealerId does not exist.")

    dealerId = int(dict["dealerId"])
    docs = []
    try:
        resp = db.get_query_result(selector={
            "dealership": {
                "$eq" : dealerId
                }
            }
            , fields=["id", "name", "car_make", "car_model", "car_year", "dealership", "purchase", "purchase_date", "review"]
            # , raw_result=True
            )
        docs = [ doc for doc in resp ]
    except CloudantException as ce:
        print("query failed.")
        return http_error(500, "query failed.")
    
    if len(docs) == 0:
        return http_error(404, "dealerId does not exist.")

    return { "body": docs }

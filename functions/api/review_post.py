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

    # POST
    fields = ["name", "car_make", "car_model", "car_year", "dealership", "purchase", "purchase_date", "review"]
    if "review" not in dict or dict["review"] is None:
        print("review does not exist.")
        return http_error(500, "something went wrong")

    doc_entry = dict["review"]
    # check if all fields are in the review block
    for field in fields:
        if field not in doc_entry:
            print(f"expected '{field}' field does not exist")
            return http_error(500, "something went wrong")
    try:
        doc = db.create_document(doc_entry)
        if not doc.exists():
            print(f"Failed to create a document given valid data {doc_entry}")
            return http_error(500, "something went wrong")
        print(f"new doc:{doc}")
    except CloudantException as ce:
        print(f"cloudant exception: {ce}")
        return http_error(500, "something went wrong")
    
    return { "body": doc["_id"] }

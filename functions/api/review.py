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
        print("Databases: {0}".format(client.all_dbs()))
        db = client.useDatabase(databaseName)
    except CloudantException as ce:
        print("unable to connect")
        return {
            "code": 500,
            "error": ce
            }
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {
            "code": 500,
            "error": err
            }

    return {"dbs": client.all_dbs()}

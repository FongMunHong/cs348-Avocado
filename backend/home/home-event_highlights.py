from asyncio.windows_events import NULL
from base64 import encode
import json
from operator import imod
import sqlalchemy as db
import datetime
from hashlib import sha256
import datetime
from datetime import date
from datetime import timedelta
import random
import sqlite3


MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "Account creation failed.", "body": {}}
MSG_ORDER_AGAIN_FAIL = {"status": 600, "statusText": "Order again table is unavailable.", "body": {}}
MSG_NO_DISC = {"status": 101, "statusText": "No discounts for today.", "body": {}}

def input_checking( func ):

    def inner( event, context ):
        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        try:
            # assert content.get( "firstName" ), "First Name not found"
            # assert content.get( "lastName" ), "Last Name not found"
            # assert content.get( "email" ), "Email not found."
            # assert content.get( "birthday" ), "Birthday not found."
            # assert content.get( "password" ), "Password not found."
            pass

        except Exception as e:
            # return data
            return { "status": 422, "statusText": "Account field missing.", "body": str( e ) }

        # return function
        return func( content, context )

    # return
    return inner

def db_connection():
    username = "admin"
    password = "avocado123"
    server = "avocado-348.cgooazgc1htx.us-east-1.rds.amazonaws.com"
    database = "avocado1"

    db_url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database)
    engine = db.create_engine(db_url, echo=False)
    engine.connect()

    return engine

@input_checking   
def lambda_handler(event, context):
    
    sql = "SELECT rest_type FROM events WHERE date = '{}'".format(datetime.datetime.today())

    #connect to db
    engine = db_connection()
    connection = engine.connect()
    rows = connection.execute(sql)

    if not rows :
        return MSG_NO_DISC
    else:
        rest_type_result = []
        for row in rows:
            rest_type_result.append(
                {
                    "rest_type": row.rest_type,
                }
        )
    
        sql = "SELECT * FROM rest_info WHERE rest_type = \"{}\"".format(rest_type_result)
        rows = connection.execute(sql)

        rests_disc = []

        for row in rows:
            rests_disc.append(
                {
                    "rest_id": row.rest_id,
                    "rest_name": row.name,
                    "rest_type": row.rest_type,
                    "rating": row.rating,
                    "img_path": row.filepath_s3
                }
            )


        try:
            return rests_disc

        except Exception as e:
            print(e)
            return MSG_ORDER_AGAIN_FAIL  




if __name__ == "__main__":
    body = {
        "date": "2022-02-28",
    }

    event = {
        "body": json.dumps(body)
    }
    context = ""

    response = lambda_handler(event, context)
    print(response)
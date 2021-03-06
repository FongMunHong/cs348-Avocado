import json
import sqlalchemy as db
import datetime
from datetime import datetime
import re
from hashlib import sha256
import uuid

MSG_REQUEST_NO_BODY = {"status": 500, "statusText": "Requests has no body.", "body": {}}
MSG_REQUEST_INCORRECT_FORMAT = {"status": 500, "statusText": "Requests incorrect format.", "body": {}}
MSG_SUCCESS = {"status": 200, "statusText": "User created account successfully.", "body": {}}
MSG_NO_FIELDS = {"status": 422, "statusText": "Missing input field.", "body": {}}
MSG_FAIL_TO_CREATE = {"status": 422, "statusText": "The account has not been created.", "body": {}}



def db_connection():
    username = "admin"
    password = "avocado123"
    server = "avocado-348.cgooazgc1htx.us-east-1.rds.amazonaws.com"
    database = "avocado1"

    db_url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database)
    engine = db.create_engine(db_url, echo=False)
    engine.connect()

    return engine


def input_checking( func ):

    def inner( event, context ):

        try:
            content = json.loads(event.get("body"))
        except:
            return MSG_REQUEST_INCORRECT_FORMAT

        """decorator for input checking"""
        # try:
        one_exception = []

        try:
            assert content.get( "name" ), "Name not found"
            assert content.get( "birthday" ), "Birthday not found."
            assert content.get( "email" ), "Email not found"
            assert content.get( "password" ), "Password not found."
            assert content.get( "confirm_password" ), "Confirm Password not found."
        except:
            return MSG_NO_FIELDS

        #name input validation
        name = content.get( "name" )

        if len(name) > 44 or len(name) < 2:
            one_exception += ["The length of the name is not the correct length."]
        
        if name.replace(" ", "").isalpha() == False:
            one_exception += ["The name needs to only contain alphabets."]


        #birthday input validation
        birthday = content.get( "birthday" )
        format = "%Y-%m-%d"

        try:
            datetime.strptime(birthday, format)
        except ValueError:
            one_exception += ["The date is not in the correct format."]

        #email input validation
        email = content.get( "email" )

        if (len(email) > 44):
            one_exception += ["The email is too long."]
        
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not(re.fullmatch(email_regex,email)):
            one_exception += ["The email is not valid."]

        #password input validation
        password = content.get( "password" )

        if( len(password) < 7):
            one_exception += ["The password needs to be more than 7 characters."]
        res = False

        for ele in password:
            if ele.isupper():
                res = True
                break
            
        if (res == False):
            one_exception += ["The password must contain at least one uppercase character."]
        
        special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:123456789]')
        
        if(special_characters.search(password) == None):
            one_exception += ["The password must contain at least one special character or a number."]
        
        confirm_password = content.get("confirm_password")

        if(password != confirm_password):
            one_exception += ["The password and the confirm password do not match."]
        
        engine = db_connection()  
        connection = engine.connect()

        sql = "SELECT user_email FROM user_info WHERE user_email = '{}'".format(content.get("email")) 
        val = connection.execute(sql).fetchone()
        if val:
            one_exception.append("The email is not unique.")

        if(len(one_exception) > 0):
            return { "status": 422, "statusText": "Account field missing.", "body": one_exception }

        # return function
        return func( content, context )

    # return
    return inner

@input_checking   
def lambda_handler(event, context):

    #retrieving from the json file 
    name = event.get('name')
    birthday =  event.get('birthday')
    email = event.get('email')
    password = event.get('password')
    
    #converting birthday to the correct format
    birthday = datetime.strptime(birthday, "%Y-%m-%d")
    birthday = birthday.strftime('%Y-%m-%d %H:%M:%S')

    #generating a unique userid
    userid = uuid.uuid4().int % 2147483647

    #hashing the password
    hashed_password = sha256(password.encode('utf-8')).hexdigest()

    # connect to db
    engine = db_connection()

    connection = engine.connect()

    try:
        sql = "INSERT INTO user_info(name, user_id, birthday, user_email, user_password) VALUES (%s, %s, %s, %s, %s)" 
        val = (name, userid, birthday, email, hashed_password)
        connection.execute(sql,val)
        return MSG_SUCCESS

    except Exception as e:
        return MSG_FAIL_TO_CREATE

if __name__ == "__main__":
    body = {
        "name": "User fifteen",
        "birthday": "2021-03-01",
        "email": "sum@c998ffof.uk",
        "password": "Pra#dji",
        "confirm_password":"Pra#dji"
    }

    event = {
        "body": json.dumps(body)
    }

    context = ""

    response = lambda_handler(event, context)
    print(response)
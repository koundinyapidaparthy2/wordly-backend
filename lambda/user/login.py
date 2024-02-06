# This is a public Rest Api where user accees are going to be taken place 

import json 
from signin import (is_valid_email, is_valid_password, user_exists_in_dynamodb)
def login_handler(event,context):
    query_parameters = event.get('queryStringParameters', {})
    user_email = query_parameters.get('email')
    user_password = query_parameters.get('password')
    headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Credentials' : True,
        'Content-Type': 'application/json'
    }
    if not is_valid_email(user_email):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error':"true",
                'message': 'Invalid email format',
            }),
            'headers': headers
        }
    if not is_valid_password(user_password):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error':"true",
                'message': 'Invalid password (must be at least 8 characters long)',
            }),
            'headers': headers
        }
    if user_exists_in_dynamodb(user_email,fromLogin=True,password=user_password):
        print(user_email)
        return {
            'statusCode': 200,
            'body': json.dumps({
                        'message': 'user logged in successfully',
                        'user_email': user_email,
                    }),
            'headers': headers
        }
    return {
        'statusCode': 400,
        'body': json.dumps({
                    'message': 'Not found',
                    'error':'true'
                }),
        'headers': headers
    } 
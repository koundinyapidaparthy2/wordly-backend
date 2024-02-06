# my_lambda.py

import json

def test_handler(event, context):
    """
    Lambda function handler.
    """
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello, AWS CDK!'}),
        'headers': {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Credentials' : True,
        'Content-Type': 'application/json'
        },
    }

    return response

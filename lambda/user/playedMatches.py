import json 
from signin import (is_valid_email, user_exists_in_dynamodb)
import boto3
from botocore.exceptions import ClientError
def user_exists_in_played_matchesdynamodb(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('matches')
    response = None
    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        response = False

    return response
def playedMatches_handler(event, context):
    query_parameters = event.get('queryStringParameters', {})
    email = query_parameters.get('email')
    headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Credentials' : True,
        'Content-Type': 'application/json'
    }
    if not is_valid_email(email):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error':"true",
                'message': 'Invalid email format',
            }),
            'headers': headers
        }
    if not user_exists_in_dynamodb(email,fromLogin=False,password=''):
        return {
            'statusCode': 400,
            'body': json.dumps({
                        'message': 'Not found',
                        'error':'true'
                    }),
            'headers': headers
        }
    response = user_exists_in_played_matchesdynamodb(email)
        
    if not response or not 'Item' in response:
        return {
            'statusCode': 500,
            'body': json.dumps({
                        'message': 'Not matches played',
                        'error':'true'
                    }),
            'headers': headers
        }
    
    else:   
        return {
        'statusCode': 200,
        'body': json.dumps({
                    'message': 'Your Matches',
                    'response': response["Item"]["result"]
                }),
        'headers': headers
    }
import json 
from signin import (is_valid_email, user_exists_in_dynamodb)
from playedMatches import user_exists_in_played_matchesdynamodb
import boto3
from botocore.exceptions import ClientError

def add_result_to_dynamodb(email, result):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('matches')
    response = None
    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )

        if 'Item' in response:
            existing_result = response['Item'].get('result', '')
            if existing_result:
                existing_result += ','  
            existing_result += result

            response = table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression="SET #result = :new_result",
                ExpressionAttributeNames={
                    "#result": "result"
                },
                ExpressionAttributeValues={
                    ":new_result": existing_result
                },
                ReturnValues="ALL_NEW" 
            )
        else:
            response = table.put_item(
                Item={
                    'email': email,
                    'result': result  
                }
            )
    except ClientError as e:
            print(e.response['Error']['Message'])
            response = False
    return response

def storeMatchResult_handler(event, context):
    query_parameters = event.get('queryStringParameters', {})
    email = query_parameters.get('email')
    result = query_parameters.get('result')
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
    if not user_exists_in_dynamodb(email, fromLogin=False,password=''):
        return {
            'statusCode': 400,
            'body': json.dumps({
                        'message': 'Not found',
                        'error':'true'
                    }),
            'headers': headers
        }
    response = add_result_to_dynamodb(email=email, result=result)
    if not response:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': "true",
                'message': 'Internal Error',
            }),
            'headers': headers
        }
      
    return {
        'statusCode': 200,
        'body': json.dumps({
                    'message': 'Matches Result Store Successfully',
                }),
        'headers': headers
    }
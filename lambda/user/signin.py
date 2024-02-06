# This is a public Rest Api where user accees are going to be taken place 

import re
import json 
import hashlib
import boto3
from botocore.exceptions import ClientError


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def is_valid_email(email):
    if email is None or not isinstance(email, str):
        return False
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    return len(password) >= 8

def is_valid_username(username):
    return len(username) >= 2

def user_exists_in_dynamodb(email, fromLogin, password):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    if fromLogin and 'Item' in response:
        stored_password = response['Item']['password']
        if hash_password(password) == stored_password:
            return True
    elif not fromLogin and 'Item' in response:
        return True
    return False

def add_user_to_dynamodb(email, password, user_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    # Hash the password before storing it
    hashed_password = hash_password(password)

    try:
        response = table.put_item(
            Item={
                'email': email,
                'password': hashed_password,
                'name': user_name
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False

    return True



def signin_handler(event,context):
    query_parameters = event.get('queryStringParameters', {})
    user_name = query_parameters.get('name')
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
    if not is_valid_username(user_name):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error':"true",
                'message': 'Invalid username (must be at least 3 characters long)',
            }),
            'headers': headers
        }
    if user_exists_in_dynamodb(user_email, fromLogin=True,password=user_password):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error':"true",
                'message': 'User with this email already exists',
            }),
            'headers': headers
        }
    if not add_user_to_dynamodb(user_email, user_password, user_name):
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
        'body': json.dumps({'message': 'user logged in successfully',
                    'user_email': user_email,
                }),
        'headers': headers
    } 
    
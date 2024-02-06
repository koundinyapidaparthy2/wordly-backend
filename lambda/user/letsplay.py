# This is a public Rest Api where user accees are going to be taken place 

import re
import random
import json 
import boto3
from signin import (is_valid_email, user_exists_in_dynamodb)
def play_handler(event,context):

    def word_to_file_name(word):
        wordNum = int(word)
        if wordNum == 5:
            return 'Five'
        elif wordNum == 6:
            return 'Six'
        elif wordNum == 7:
            return 'Seven'
        elif wordNum == 8:
            return 'Eight'
    query_parameters = event.get('queryStringParameters', {})
    user_email = query_parameters.get('email')
    word = query_parameters.get('word')
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
    if not user_exists_in_dynamodb(user_email, fromLogin=False,password=''):
        return {
            'statusCode': 400,
            'body': json.dumps({
                        'message': 'Not found',
                        'error':'true'
                    }),
            'headers': headers
        }
    
    fileWord = word_to_file_name(word)
    s3_bucket_name = "wordsfilelist-for-wordly-2024"
    s3_client = boto3.client('s3')

    try:
        s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=f"WordlyList/{fileWord}_Letter_Word_List.txt")
        object_content = s3_object['Body'].read().decode('utf-8')
        if object_content:
            words_list =   object_content.split("\n")
            filterWordsList =  [item for item in words_list if bool(item)]
            if isinstance(word, str):
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Word for play',
                        'choiceword': random.choice(filterWordsList)
                    }),
                    'headers': headers
                }
            else:
                return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': "true",
                    'message': 'Internal word error',
                }),
                'headers': headers
            }
            
        else:
            return {
            'statusCode': 500,
            'body': json.dumps({
                'error': "true",
                'message': 'Internal File Issue',
            }),
            'headers': headers
        }
            

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': "true",
                'message': f'Error retrieving S3 object: {str(e)}',
            }),
            'headers': headers
        }
    

from http import HTTPStatus
import json
import os
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):

    data = json.loads(event['body'])

    status_code = HTTPStatus.OK
    body_message = ""

    try:
        todo_res = todo_tbl.query(
            KeyConditionExpression=Key("login_token").eq(data["login_token"]),
            ConsistentRead=True
        )
        print("INFO: todo find")
        print(todo_res)
        body_message = todo_res['Items']
        print(body_message)


    except Exception as e:
        print(e)
        print("ERROR: table not found.")
        status_code = HTTPStatus.NOT_FOUND

    return {
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(body_message)
    }

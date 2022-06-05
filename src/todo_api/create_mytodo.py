from http import HTTPStatus
import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):
    print(json.dumps(event))

    data = json.loads(event['body'])
    # 本当はバリデーションが必要

    todo = {
        'login_id': data["login_id"],
        'todo_id': str(uuid.uuid4()),
        'title': data['title']
    }

    todo_tbl.put_item(Item=todo)

    return {
        "statusCode": HTTPStatus.OK,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(todo)
    }




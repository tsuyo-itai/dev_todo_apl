from http import HTTPStatus
import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):

    '''
    ## bodyの期待値
    body = {
        "login_token": ログインユーザーのトークン,
        "todo_title": ログインに必要なPASS,
        'todo_details': data['todo_details']
    }
    '''
    data = json.loads(event['body'])

    # 本当はバリデーションが必要

    todo = {
        'login_token': data["login_token"],
        'todo_id': str(uuid.uuid4()),
        'todo_title': data['todo_title'],
        'todo_details': data['todo_details']
    }

    # DBへTODOを登録
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




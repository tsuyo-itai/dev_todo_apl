from http import HTTPStatus
import json
import os
import boto3
import uuid

# 使用するDBの定義
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):

    '''
    ## bodyの期待値
    body = {
        "login_token": ログインユーザーのトークン,
        "todo_title": TODOのタイトル,
        'todo_details': TODOの内容
    }
    '''
    data = json.loads(event['body'])

    # 応答情報の初期化
    status_code = HTTPStatus.CREATED
    body_message = ""

    # 本当はバリデーションが必要

    try:
        # 作成するToDo情報
        todo = {
            'login_token': data["login_token"],
            'todo_id': str(uuid.uuid4()),
            'todo_title': data['todo_title'],
            'todo_details': data['todo_details']
        }

        # DBへTODOを登録
        todo_tbl.put_item(Item=todo)

        # レスポンス用
        body_message = todo

    except Exception as e:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        body_message = {"message": "Internal Server Error"}

    return {
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(body_message)
    }




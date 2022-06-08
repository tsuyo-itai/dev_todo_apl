from http import HTTPStatus
import json
import os
import boto3
from boto3.dynamodb.conditions import Key

# 使用するDBの定義
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):
    '''
    ## bodyの期待値
    body = {
        "login_token": ログインユーザーのトークン,
        "search_word": 検索キーワード
    }
    '''
    data = json.loads(event['body'])

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = []

    try:
        todo_res = todo_tbl.query(
            KeyConditionExpression=Key('login_token').eq(data['login_token'])
        )

        for todo_data in todo_res['Items']:
            # タイトルに検索ワードが含まれるか
            if data['search_word'] in todo_data['todo_title']:
                body_message.append(todo_data)
                continue
            
            # 内容に検索ワードが含まれるか
            if data['search_word'] in todo_data['todo_details']:
                body_message.append(todo_data)
                continue

    except Exception as e:
        #TODO どのような例外が起こる可能性があるか? それに適した処理が必要か
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return {
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps({"todos": body_message})
    }


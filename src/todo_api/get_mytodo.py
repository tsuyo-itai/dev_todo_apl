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
        "login_token": ログインユーザーのトークン
    }
    '''
    data = json.loads(event['body'])

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = []

    try:
        todo_res = todo_tbl.query(
            KeyConditionExpression=Key("login_token").eq(data["login_token"]),
            ConsistentRead=True
        )
        body_message = todo_res['Items']


    except Exception as e:
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

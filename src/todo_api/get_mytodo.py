from http import HTTPStatus
import json
import os
import boto3
import uuid
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
    login_token = data["login_token"]

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = []

    try:
        if ValidationDatas(login_token):
            ## バリデーションOK
            todo_res = todo_tbl.query(
                KeyConditionExpression=Key("login_token").eq(login_token),
                ConsistentRead=True
            )
            body_message = todo_res['Items']

        else:
            ## バリデーションNG
            status_code = HTTPStatus.BAD_REQUEST

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


'''-------------------------------------------------
@ バリデーション関数
@ in        login_token: ログイントークン
@ return    バリデーションOK: True  バリデーションNG:False
-------------------------------------------------'''
def ValidationDatas(login_token):
    # UUIDの形式であるか
    try:
        uuid.UUID(login_token, version=4)
    except:
        return False

    return True

from http import HTTPStatus
import json
import os
import boto3
from boto3.dynamodb.conditions import Key
import uuid

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
    login_token = data['login_token']
    search_word = data['search_word']

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = []

    try:
        if ValidationDatas(login_token, search_word):
            ## バリデーションOK
            todo_res = todo_tbl.query(
                KeyConditionExpression=Key('login_token').eq(login_token)
            )

            for todo_data in todo_res['Items']:
                # タイトルに検索ワードが含まれるか
                if search_word in todo_data['todo_title']:
                    body_message.append(todo_data)
                    continue
                
                # 内容に検索ワードが含まれるか
                if search_word in todo_data['todo_details']:
                    body_message.append(todo_data)
                    continue
        else:
            ## バリデーションNG
            status_code = HTTPStatus.BAD_REQUEST

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


'''-------------------------------------------------
@ バリデーション関数
@ in        login_token: ログイントークン
            search_word: 検索ワード
@ return    バリデーションOK: True  バリデーションNG:False
-------------------------------------------------'''
def ValidationDatas(login_token, search_word):
    # UUIDの形式であるか
    try:
        uuid.UUID(login_token, version=4)
    except:
        return False
    
    # 最大許容文字数512文字までとする
    if not (0 < len(search_word) and len(search_word) <= 512):
        return False

    return True
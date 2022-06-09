from http import HTTPStatus
import os
import boto3
import json
import uuid

# 使用するDBの定義
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):

    '''
    ## bodyの期待値
    body = {
        "login_token": ログインユーザーのトークン,
        "todo_id": TODOのID
    }
    '''
    data = json.loads(event['body'])
    login_token = data["login_token"]
    todo_id = data["todo_id"]

    # 応答情報の初期化
    status_code = HTTPStatus.NO_CONTENT
    body_message = ""

    try:
        if ValidationDatas(login_token, todo_id):
            ## バリデーションOK
            # DBからToDoを削除
            todo_tbl.delete_item(Key={'todo_id': todo_id, 'login_token': login_token})
        else:
            ## バリデーションNG
            status_code = HTTPStatus.BAD_REQUEST
            body_message = {"message": "入力された値が不正です"}

    except Exception as e:
        #TODO どのような例外が起こる可能性があるか? それに適した処理が必要か
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


'''-------------------------------------------------
@ バリデーション関数
@ in        login_token: ログイントークン
            todo_id: ToDoのID
@ return    バリデーションOK: True  バリデーションNG:False
-------------------------------------------------'''
def ValidationDatas(login_token, todo_id):
    # UUIDの形式であるか
    try:
        uuid.UUID(login_token, version=4)
        uuid.UUID(todo_id, version=4)
    except:
        return False

    return True
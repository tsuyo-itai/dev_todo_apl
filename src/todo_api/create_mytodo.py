from http import HTTPStatus
import json
import os
import boto3
import uuid
from datetime import datetime

# 使用するDBの定義
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):

    '''
    ## bodyの期待値
    body = {
        "login_token": ログインユーザーのトークン,
        "todo_title": TODOのタイトル,
        "todo_details": TODOの内容,
        "todo_expired_at_unix_time": TODOの期限 (設定しない場合は不要)
    }
    '''
    data = json.loads(event['body'])

    login_token = data["login_token"]
    todo_title = data['todo_title']
    todo_details = data['todo_details']
     # ToDoの期限設定があるか?
    if 'todo_expired_at_unix_time' in data:
        todo_expired_at_unix_time = data['todo_expired_at_unix_time']
    else:
        todo_expired_at_unix_time = None

    # 応答情報の初期化
    status_code = HTTPStatus.CREATED
    body_message = ""

    try:
        if ValidationDatas(todo_title, todo_details, todo_expired_at_unix_time):
            ## バリデーションOK
            if todo_expired_at_unix_time is not None:
                # 作成するToDo情報 (TODO期限も付与)
                todo = {
                    'login_token': login_token,
                    'todo_id': str(uuid.uuid4()),
                    'todo_title': todo_title,
                    'todo_details': todo_details,
                    'todo_expired_at_unix_time': todo_expired_at_unix_time
                }

            else:
                # 作成するToDo情報
                todo = {
                    'login_token': login_token,
                    'todo_id': str(uuid.uuid4()),
                    'todo_title': todo_title,
                    'todo_details': todo_details
                }

            # DBへTODOを登録
            todo_tbl.put_item(Item=todo)

            # レスポンス用
            body_message = todo

        else:
            ## バリデーションNG
            status_code = HTTPStatus.BAD_REQUEST
            body_message = {"message": "入力された値が不正です"}

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


'''-------------------------------------------------
@ バリデーション関数
@ in        todo_title: ToDOのタイトル
            todo_details: ToDoの内容
            todo_expired_at_unix_time: ToDoの有効期限
@ return    バリデーションOK: True  バリデーションNG:False
-------------------------------------------------'''
def ValidationDatas(todo_title, todo_details, todo_expired_at_unix_time):
    # タイトルは256文字までとする
    if not (0 < len(todo_title) and len(todo_title) <= 256):
        return False

    # 内容は512文字までとする
    if not (0 < len(todo_details) and len(todo_details) <= 512):
        return False
    
    if todo_expired_at_unix_time is not None:
        # UNIX時間であるか
        try:
            datetime.fromtimestamp(int(todo_expired_at_unix_time))
        except:
            # 変換に失敗した場合はUNIX時間の形式ではない
            return False

    return True





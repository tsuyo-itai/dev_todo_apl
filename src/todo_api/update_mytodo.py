from http import HTTPStatus
import os
import boto3
import json
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
        "todo_id": TODOのID,
        "todo_title": TODOのタイトル,
        "todo_details": TODOの内容,
        "todo_expired_at_unix_time": TODOの期限 (設定しない場合は不要)
    }
    '''
    data = json.loads(event['body'])
    login_token = data['login_token']
    todo_id = data['todo_id']
    todo_title = data['todo_title']
    todo_details = data['todo_details']
     # ToDoの期限設定があるか?
    if 'todo_expired_at_unix_time' in data:
        todo_expired_at_unix_time = data['todo_expired_at_unix_time']
    else:
        todo_expired_at_unix_time = None

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = ""

    try:
        if ValidationDatas(login_token, todo_id, todo_title, todo_details, todo_expired_at_unix_time):
            #TODO 指定したtodoIDのチェック
            todo_res = todo_tbl.get_item(Key={"login_token": login_token, "todo_id": todo_id})

            if "Item" in todo_res:
                # todoが存在する
                # 更新用データの設定
                if todo_expired_at_unix_time is not None:
                    # ToDo期限設定がある場合のフォーマット
                    options = {
                        'Key': {"login_token": login_token, "todo_id": todo_id},
                        "UpdateExpression": "set #todo_title = :todo_title, #todo_details = :todo_details, #todo_expired_at_unix_time = :todo_expired_at_unix_time",
                        "ExpressionAttributeNames": {
                            "#todo_title": "todo_title",
                            "#todo_details": "todo_details",
                            "#todo_expired_at_unix_time": "todo_expired_at_unix_time"
                        },
                        "ExpressionAttributeValues": {
                            ":todo_title": todo_title,
                            ":todo_details": todo_details,
                            ":todo_expired_at_unix_time": todo_expired_at_unix_time,
                        }
                    }
                else:
                    # ToDo期限設定がない場合のフォーマット
                    options = {
                        'Key': {"login_token": login_token, "todo_id": todo_id},
                        "UpdateExpression": "set #todo_title = :todo_title, #todo_details = :todo_details",
                        "ExpressionAttributeNames": {
                            "#todo_title": "todo_title",
                            "#todo_details": "todo_details"
                        },
                        "ExpressionAttributeValues": {
                            ":todo_title": todo_title,
                            ":todo_details": todo_details,
                        }
                    }

                # DBのToDoを更新
                todo_tbl.update_item(**options)

                # 更新後のtodoを取得
                todo_res = todo_tbl.get_item(Key={"login_token": login_token, "todo_id": todo_id})
                body_message = todo_res['Item']

            else:
                # 1件もhitしない場合
                status_code = HTTPStatus.NOT_FOUND
                body_message = {"message": "指定のToDoが見つかりませんでした"}
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
            todo_title: ToDoのタイトル
            todo_details: ToDoの内容
            todo_expired_at_unix_time: ToDoの有効期限
@ return    バリデーションOK: True  バリデーションNG:False
-------------------------------------------------'''
def ValidationDatas(login_token, todo_id, todo_title, todo_details, todo_expired_at_unix_time):
    # UUIDの形式であるか
    try:
        uuid.UUID(login_token, version=4)
        uuid.UUID(todo_id, version=4)
    except:
        return False
    
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
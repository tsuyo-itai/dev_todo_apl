from http import HTTPStatus
import os
import boto3
import json

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
        'todo_details': TODOの内容
    }
    '''
    data = json.loads(event['body'])

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = ""

    try:
        #TODO 指定したtodoIDのチェック
        todo_res = todo_tbl.get_item(Key={"login_token": data["login_token"], "todo_id": data["todo_id"]})

        if "Item" in todo_res:
            # todoが存在する
            # 更新用データの設定
            options = {
                'Key': {"login_token": data["login_token"], "todo_id": data["todo_id"]},
                "UpdateExpression": "set #todo_title = :todo_title, #todo_details = :todo_details",
                "ExpressionAttributeNames": {
                    "#todo_title": "todo_title",
                    "#todo_details": "todo_details"
                },
                "ExpressionAttributeValues": {
                    ":todo_title": data['todo_title'],
                    ":todo_details": data['todo_details'],
                }
            }

            # DBのToDoを更新
            todo_tbl.update_item(**options)

            # 更新後のtodoを取得
            todo_res = todo_tbl.get_item(Key={"login_token": data["login_token"], "todo_id": data["todo_id"]})
            body_message = todo_res['Item']

        else:
            # 1件もhitしない場合
            status_code = HTTPStatus.NOT_FOUND
            body_message = {"message": "指定のToDoが見つかりませんでした"}

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
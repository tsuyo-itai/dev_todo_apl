from http import HTTPStatus
import boto3
import sys
import uuid
from datetime import datetime


# 使用するDBの定義
table_name="TODO_TABLE"
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(table_name)

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


if __name__ == "__main__": 

    # 引数から送信データを作成
    args = sys.argv

    if (len(args) != 5 and len(args) != 6):
        print("引数エラー")
        print("第1引数: login_token")
        print("第2引数: todo_id")
        print("第3引数: todo_title")
        print("第4引数: todo_details")
        print("(第5引数: todo_expired_at_unix_time)")
        sys.exit()

    login_token = args[1]
    todo_id = args[2]
    todo_title = args[3]
    todo_details = args[4]
     # ToDoの期限設定があるか?
    if len(args) == 6 :
        todo_expired_at_unix_time = args[5]
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


    print({
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": body_message
    })
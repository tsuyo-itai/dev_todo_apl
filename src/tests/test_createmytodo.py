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


if __name__ == "__main__": 

    # 引数から送信データを作成
    args = sys.argv

    if (len(args) != 4 and len(args) != 5):
        print("引数エラー")
        print("第1引数: login_token")
        print("第2引数: todo_title")
        print("第3引数: todo_details")
        print("(第4引数: todo_expired_at_unix_time)")
        sys.exit()

    login_token = args[1]
    todo_title = args[2]
    todo_details = args[3]
     # ToDoの期限設定があるか?
    if len(args) == 5 :
        todo_expired_at_unix_time = args[4]
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

    print( {
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": body_message
    })

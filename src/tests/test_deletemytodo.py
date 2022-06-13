from http import HTTPStatus
import boto3
import sys
import uuid


# 使用するDBの定義
table_name="TODO_TABLE"
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(table_name)

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


if __name__ == "__main__": 

    # 引数から送信データを作成
    args = sys.argv

    if (len(args) != 3):
        print("引数エラー")
        print("第1引数: login_token")
        print("第2引数: todo_id")
        sys.exit()

    login_token = args[1]
    todo_id = args[2]

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


    print({
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": body_message
    })

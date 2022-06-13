from http import HTTPStatus
import boto3
import sys
import uuid
from boto3.dynamodb.conditions import Key


# 使用するDBの定義
table_name="TODO_TABLE"
dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(table_name)

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


if __name__ == "__main__": 

    # 引数から送信データを作成
    args = sys.argv

    if (len(args) != 2):
        print("引数エラー")
        print("第1引数: login_token")
        sys.exit()

    login_token = args[1]

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

    print({
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": {"todos": body_message}
    })

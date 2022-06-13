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


if __name__ == "__main__": 

    # 引数から送信データを作成
    args = sys.argv

    if (len(args) != 3):
        print("引数エラー")
        print("第1引数: login_token")
        print("第2引数: search_word")
        sys.exit()

    login_token = args[1]
    search_word = args[2]

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

    print({
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": {"todos": body_message}
    })

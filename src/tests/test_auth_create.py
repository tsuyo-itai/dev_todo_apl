from http import HTTPStatus
import boto3
import sys
import uuid
from scryp import encrypt

# 使用するDBの定義
table_name="AUTH_TABLE"
dynamodb = boto3.resource('dynamodb')
auth_tbl = dynamodb.Table(table_name)

'''-------------------------------------------------
@ バリデーション関数
@ in        login_id: ログインID
            login_pass: ログインパスワード
@ return    バリデーションOK: True  バリデーションNG:False
-------------------------------------------------'''
def ValidationDatas(login_id, login_pass):
    # ログインIDは36文字までとする
    if not (0 < len(login_id) and len(login_id) <= 36):
        return False

    # ログインPASSは36文字までとする
    if not (0 < len(login_pass) and len(login_pass) <= 36):
        return False

    return True


if __name__ == "__main__": 

    # 暗号化のためのシークレットキー
    secret_key = "secret_key_todoapl"

    # 引数から送信データを作成
    args = sys.argv

    if (len(args) != 3):
        print("引数エラー")
        print("第1引数: login_id")
        print("第2引数: login_pass")
        sys.exit()

    login_id = args[1]
    login_pass = args[2]

    # 応答情報の初期化
    status_code = HTTPStatus.CREATED
    body_message = ""

    try:
        if ValidationDatas(login_id, login_pass):
            # 指定したログインIDは存在するか?
            auth_tbl_res = auth_tbl.get_item(Key={"login_id": login_id})

            # 取得結果はItemプロパティに格納される
            if "Item" in auth_tbl_res:
                # 既にログインIDは存在するのでユーザー作成は行わない
                status_code = HTTPStatus.CONFLICT
                body_message = {"message": "既にユーザー登録済みです"}

            else:

                # ログインIDは存在しないのでユーザー登録
                user_data = {
                    'login_id': login_id,
                    'login_pass': encrypt(login_pass, secret_key),
                    'login_token': str(uuid.uuid4())
                }
                # DBへユーザー情報を登録
                auth_tbl.put_item(Item=user_data)
                # responceにユーザー情報を設定
                body_message = user_data

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


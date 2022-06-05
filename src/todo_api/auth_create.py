from http import HTTPStatus
import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
auth_tbl = dynamodb.Table(os.environ['AUTH_TBL'])

def lambda_handler(event, context):

    '''
    ## bodyの期待値
    body = {
        "login_id": ログインに必要なID,
        "login_pass": ログインに必要なPASS
    }
    '''
    data = json.loads(event['body'])

    # 応答情報の初期化
    status_code = HTTPStatus.OK
    body_message = ""

    try:
        # 指定したログインIDは存在するか?
        auth_tbl_res = auth_tbl.get_item(Key={"login_id": data['login_id']})

        # 取得結果はItemプロパティに格納される
        if "Item" in auth_tbl_res:
            # 既にログインIDは存在するのでユーザー作成は行わない
            print("【DEBUG】すでに登録済み")
            # TODO ステータスコードは妥当か?
            status_code = HTTPStatus.CONFLICT 
            body_message = "既にユーザー登録済みです"

        else:
            # ログインIDは存在しないのでユーザー登録
            print("【DEBUG】ユーザー登録実行")

            user_data = {
                'login_id': data['login_id'],
                'login_pass': data['login_pass'],
                'login_token': str(uuid.uuid4())
            }
            # DBへユーザー情報を登録
            auth_tbl.put_item(Item=user_data)
            print("【INFO】ユーザー登録完了")
            body_message = json.dumps(user_data)

    except Exception as e:
        print("【DEBUG】例外によるNG")
        #TODO どのような例外が起こる可能性があるか? それに適した処理が必要か
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        body_message = "何らかの原因で失敗しました"


    return {
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": body_message
    }


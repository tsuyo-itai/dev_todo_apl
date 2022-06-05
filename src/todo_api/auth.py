from http import HTTPStatus
import json
import os
import boto3

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
            # ログインIDがhitした場合
            login_data = auth_tbl_res['Item']
            # パスワードの照合
            if login_data['login_pass'] == data['login_pass']:
                # パスワードOK
                print("【DEBUG】認証OK")

            else:
                # パスワードNG
                print("【DEBUG】認証NG (パスワードNG)")
                status_code = HTTPStatus.UNAUTHORIZED
                body_message = "パスワードに誤りがあります"

        else:
            # ログインIDがhitしなかった場合
            print("【DEBUG】認証NG (ユーザーNG)")
            status_code = HTTPStatus.UNAUTHORIZED
            body_message = "ユーザー登録を行ってください"


    except Exception as e:
        print("【DEBUG】例外によるNG")
        #TODO どのような例外が起こる可能性があるか? それに適した処理が必要か
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        body_message = "ユーザー登録を行ってください"


    return {
        "statusCode": status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": body_message
    }
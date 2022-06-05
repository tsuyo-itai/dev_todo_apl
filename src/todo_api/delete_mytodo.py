import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(os.environ['TODO_TBL'])

def lambda_handler(event, context):

    '''
    ## bodyの期待値
    body = {
        "login_token": ログインユーザーのトークン,
    }
    '''
    data = json.loads(event['body'])

    # IDはURLから取得する (bodyでdataで送信しても良い)
    todo_id = event['pathParameters']['todo_id']

    #TODO 指定したtodoIDのチェック

    # DBからToDoを削除
    todo_tbl.delete_item(Key={'todo_id': todo_id, 'login_token': data["login_token"]})

    return {
        "statusCode": 204,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": '削除OK'
    }
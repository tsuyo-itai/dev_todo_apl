from http import HTTPStatus
import json
import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key


#-------以下はtest以外は不要 ---------
import sys
#-------

table_name="TODO_TABLE"

dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(table_name)

#! ほしい情報は login_tokenとtodo_id
#-------以下はtest以外は不要 ---------
args = sys.argv

if (len(args) != 3):
    print("引数エラー")
    sys.exit()
#-------
print(args[1])
print(args[2])



try:
    # 応答データを格納するため用意
    res_datas = []

    todo_res = todo_tbl.query(
        KeyConditionExpression=Key('login_token').eq(args[1])
    )

    for todo_data in todo_res['Items']:

        # タイトルに検索ワードが含まれるか
        if args[2] in todo_data['todo_title']:
            res_datas.append(todo_data)
            continue
        
        # 内容に検索ワードが含まれるか
        if args[2] in todo_data['todo_details']:
            res_datas.append(todo_data)
            continue

    print(res_datas)





except Exception as e:
    print(e)
    print("ERROR: table not found.")


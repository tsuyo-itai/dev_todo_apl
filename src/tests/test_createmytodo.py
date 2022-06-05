from http import HTTPStatus
import json
import os
import boto3
import uuid

#-------以下はtest以外は不要 ---------
import sys
#-------

table_name="TODO_TABLE"

dynamodb = boto3.resource('dynamodb')
todo_tbl = dynamodb.Table(table_name)


#! ほしい情報は login_idとtodoのタイトル
#-------以下はtest以外は不要 ---------
args = sys.argv

if (len(args) != 3):
    print("引数エラー")
    sys.exit()
#-------

try:
    # todoの作成
    todo = {
        'login_id': args[1],
        'todo_id': str(uuid.uuid4()),
        'title': args[2]
    }

    todo_tbl.put_item(Item=todo)


except Exception as e:
    print(e)
    print("ERROR: table not found.")


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

#! ほしい情報は login_id
#-------以下はtest以外は不要 ---------
args = sys.argv

if (len(args) != 2):
    print("引数エラー")
    sys.exit()
#-------

try:
    todo_res = todo_tbl.get_item(Key={"login_id": args[1]})
    if "Item" in todo_res:
        # 登録不可
        print("INFO: todo find")
        print(todo_res['Item'])

    else:
        # 1件もhitしない場合
        print("INFO: todo not found")


except Exception as e:
    print(e)
    print("ERROR: table not found.")


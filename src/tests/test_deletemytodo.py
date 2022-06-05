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

#! ほしい情報は login_idとtodo_id
#-------以下はtest以外は不要 ---------
args = sys.argv

if (len(args) != 3):
    print("引数エラー")
    sys.exit()
#-------
print(args[1])
print(args[2])


try:
    # id管理がUUIDなのでログインIDと照らし合わせる必要はない？
    todo_tbl.delete_item(
        Key={
            'login_id': args[1],
            'todo_id' : args[2]
        })


except Exception as e:
    print(e)
    print("ERROR: table not found.")


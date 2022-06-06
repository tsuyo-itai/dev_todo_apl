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

#! ほしい情報は login_tokenとtodo_id
#-------以下はtest以外は不要 ---------
args = sys.argv

if (len(args) != 5):
    print("引数エラー")
    sys.exit()
#-------
print(args[1])
print(args[2])

options = {
    'Key': {"login_token": args[1], "todo_id": args[2]},
    "UpdateExpression": "set #todo_title = :todo_title, #todo_details = :todo_details",
    "ExpressionAttributeNames": {
        "#todo_title": "todo_title",
        "#todo_details": "todo_details"
    },
    "ExpressionAttributeValues": {
        ":todo_title": args[3],
        ":todo_details": args[4],
    }
}

try:
    todo_res = todo_tbl.get_item(Key={"login_token": args[1], "todo_id": args[2]})
    if "Item" in todo_res:
        # todoが存在する
        print("【INFO】todo find")
        print(todo_res['Item'])
        # todoを更新する
        todo_tbl.update_item(**options)
        # 更新後のtodoを出力
        todo_res = todo_tbl.get_item(Key={"login_token": args[1], "todo_id": args[2]})
        print(todo_res['Item'], type(todo_res['Item']))
        print(json.dumps(todo_res['Item']), type(json.dumps(todo_res['Item'])))

    else:
        # 1件もhitしない場合
        print("INFO: todo not found")


except Exception as e:
    print(e)
    print("ERROR: table not found.")


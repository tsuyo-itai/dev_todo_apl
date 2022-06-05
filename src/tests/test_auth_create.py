from http import HTTPStatus
import json
import os
import boto3
import uuid

#-------以下はtest以外は不要 ---------
import sys
#-------

table_name="AUTH_TABLE"

dynamodb = boto3.resource('dynamodb')
auth_tbl = dynamodb.Table(table_name)

#! ほしい情報は login_idとpassword
#-------以下はtest以外は不要 ---------
args = sys.argv

if (len(args) != 3):
    print("引数エラー")
    sys.exit()
#-------
try:
    auth_res = auth_tbl.get_item(Key={"login_id": args[1]})
    if "Item" in auth_res:
        # 登録不可
        print("INFO: already regist.")
        sys.exit()

    else:
        # 1件もhitしない場合
        # 登録可能
        print("INFO: not regist.")

        user_data = {
            'login_id': args[1],
            'login_pass': args[2],
        }

        auth_tbl.put_item(Item=user_data)
        print("INFO: regist ok!")

except Exception as e:
    print(e)
    print("ERROR: table not found.")


FORMAT: 1A

# Group ユーザー管理

## ToDo管理ユーザ作成のエンドポイント [/Prod/auth/create]

### ToDo管理ユーザ登録API [POST]

#### 処理概要

* ToDo管理ユーザーの新規作成を行う.
* 登録成功時に、登録ユーザー情報を返す.

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_id: abc123 (string, required) - ログインID(format: string) - ログインIDの上限は36文字
        + login_pass: pass1234 (string, required) - ログインパスワード(format: string) - ログインPASSの上限は36文字

+ Response 201 (application/json)

    + Attributes
        + login_id: abc123 (string, required) - ログインID(format: string) - ログインIDの上限は36文字
        + login_pass: pass1234 (string, required) - ログインパスワード(format: string) - ログインPASSの上限は36文字
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)

+ Response 400 (application/json)

    + Attributes
        + message: `入力された値が不正です` (string, required) - エラーメッセージ(format: string)

+ Response 409 (application/json)

    + Attributes
        + message: 既にユーザー登録済みです (string, required) - エラーメッセージ(format: string)

+ Response 500 (application/json)

    + Attributes
        + message: `Internal Server Error` (string, required) - エラーメッセージ(format: string)

# Group ユーザー管理

## ToDo管理ユーザログインのエンドポイント [/Prod/auth]

### ToDo管理ユーザログインAPI [POST]

#### 処理概要

* ToDo管理ユーザーのログインを行う.
* ログイン成功時に、ユーザーのログイントークンを返す.
　(以降ログイントークンとToDo情報が紐付けられる)

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_id: abc123 (string, required) - ログインID(format: string) - ログインIDの上限は36文字
        + login_pass: pass1234 (string, required) - ログインパスワード(format: string) - ログインPASSの上限は36文字

+ Response 200 (application/json)

    + Attributes
        + login_id: `abc123` (string, required) - ログインID(format: string) - ログインIDの上限は36文字
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)

+ Response 400 (application/json)

    + Attributes
        + message: `入力された値が不正です` (string, required) - エラーメッセージ(format: string)

+ Response 401 (application/json)

    + Attributes
        + message: ログインIDまたはパスワードに誤りがあります (string, required) - エラーメッセージ(format: string)

+ Response 500 (application/json)

    + Attributes
        + message: `Internal Server Error` (string, required) - エラーメッセージ(format: string)

# Group TODO管理

## ToDo取得のエンドポイント [/Prod/todos]

### ToDo取得API [POST]

#### 処理概要

* 自ユーザーのToDoの取得を行う.

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)

+ Response 200 (application/json)

    + Attributes
        + todos (array[object], fixed-type)
             + (object)
                 + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
                 + todo_id: `c0abebfd-0f27-44d4-8d39-7e8d67b937e6` (string, required) - ToDoID(format: uuid)
                 + todo_title: hogehoge (string, required) - ToDoのタイトル(format: string) - タイトルの上限は256文字
                 + todo_details: hugahuga (string, required) - ToDoの内容(format: string) - 内容の上限は512文字
                 + todo_expired_at_unix_time : 1655442000 (string) - ToDoの期限 unix時間(format: string)

+ Response 400 (application/json)

    + Attributes
        + todos: [] (array[], fixed-type)

+ Response 500 (application/json)

    + Attributes
        + todos: [] (array[], fixed-type)FORMAT: 1A

# Group TODO管理

## ToDo作成のエンドポイント [/Prod/todos/create]

### ToDo作成API [POST]

#### 処理概要

* ToDoの作成を行う.

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
        + todo_title: hogehoge (string, required) - ToDoのタイトル(format: string) - タイトルの上限は256文字
        + todo_details: hugahuga (string, required) - ToDoの内容(format: string) - 内容の上限は512文字
        + todo_expired_at_unix_time : 1655442000 (string) - ToDoの期限 unix時間(format: string)

+ Response 201 (application/json)

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
        + todo_id: `c0abebfd-0f27-44d4-8d39-7e8d67b937e6` (string, required) - ToDoID(format: uuid)
        + todo_title: hogehoge (string, required) - ToDoのタイトル(format: string) - タイトルの上限は256文字
        + todo_details: hugahuga (string, required) - ToDoの内容(format: string) - 内容の上限は512文字
        + todo_expired_at_unix_time : 1655442000 (string) - ToDoの期限 unix時間(format: string)

+ Response 400 (application/json)

    + Attributes
        + message: `入力された値が不正です` (string, required) - エラーメッセージ(format: string)

+ Response 500 (application/json)

    + Attributes
        + message: `Internal Server Error` (string, required) - エラーメッセージ(format: string)

# Group TODO管理

## ToDo削除のエンドポイント [/Prod/todos]

### ToDo削除API [DELETE]

#### 処理概要

* ToDoの削除を行う.

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
        + todo_id: `c0abebfd-0f27-44d4-8d39-7e8d67b937e6` (string, required) - ToDoID(format: uuid)

+ Response 204 (application/json)

    + Attributes

+ Response 400 (application/json)

    + Attributes
        + message: `入力された値が不正です` (string, required) - エラーメッセージ(format: string)

+ Response 500 (application/json)

    + Attributes
        + message: `Internal Server Error` (string, required) - エラーメッセージ(format: string)

# Group TODO管理

## ToDo更新のエンドポイント [/Prod/todos]

### ToDo更新API [PUT]

#### 処理概要

* ToDoの更新(編集)を行う.

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
        + todo_id: `c0abebfd-0f27-44d4-8d39-7e8d67b937e6` (string, required) - ToDoID(format: uuid)
        + todo_title: hogehoge (string, required) - ToDoのタイトル(format: string) - タイトルの上限は256文字
        + todo_details: hugahuga (string, required) - ToDoの内容(format: string) - 内容の上限は512文字
        + todo_expired_at_unix_time : 1655442000 (string) - ToDoの期限 unix時間(format: string)


+ Response 200 (application/json)

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
        + todo_id: `c0abebfd-0f27-44d4-8d39-7e8d67b937e6` (string, required) - ToDoID(format: uuid)
        + todo_title: hogehoge (string, required) - ToDoのタイトル(format: string) - タイトルの上限は256文字
        + todo_details: hugahuga (string, required) - ToDoの内容(format: string) - 内容の上限は512文字
        + todo_expired_at_unix_time : 1655442000 (string) - ToDoの期限 unix時間(format: string)

+ Response 400 (application/json)

    + Attributes
        + message: `入力された値が不正です` (string, required) - エラーメッセージ(format: string)

+ Response 404 (application/json)

    + Attributes
        + message: 指定のToDoが見つかりませんでした (string, required) - エラーメッセージ(format: string)

+ Response 500 (application/json)

    + Attributes
        + message: `Internal Server Error` (string, required) - エラーメッセージ(format: string)

# Group TODO管理

## ToDo検索のエンドポイント [/Prod/todos/search]

### ToDo検索API [POST]

#### 処理概要

* ToDoの検索を行う.
* 検索対象はToDoのタイトルと内容 (部分一致)

+ Request (application/json)

    + Headers

            Accept: application/json

    + Attributes
        + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
        + search_word: hogehoge (string, required) - 検索ワード(format: string) - 検索ワード上限は512文字

+ Response 200 (application/json)

    + Attributes
        + todos (array[object], fixed-type)
             + (object)
                + login_token: `1a772109-3694-42c9-9e2e-f141e789fd84` (string, required) - ログイントークン(format: uuid)
                + todo_id: `c0abebfd-0f27-44d4-8d39-7e8d67b937e6` (string, required) - ToDoID(format: uuid)
                + todo_title: hogehoge (string, required) - ToDoのタイトル(format: string) - タイトルの上限は256文字
                + todo_details: hugahuga (string, required) - ToDoの内容(format: string) - 内容の上限は512文字
                + todo_expired_at_unix_time : 1655442000 (string) - ToDoの期限 unix時間(format: string)

+ Response 400 (application/json)

    + Attributes
        + todos: [] (array[], fixed-type)

+ Response 500 (application/json)

    + Attributes
        + todos: [] (array[], fixed-type)

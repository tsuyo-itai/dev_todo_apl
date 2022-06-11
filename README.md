# dev_todo_apl

## RESTAPIのセットアップ

Macのターミナルから実行

### 必要なモジュール類のインストール

```
$ pip install aws-sam-cli
```


### AWS認証情報の設定
事前にアクセスキーIDとシークレットキーIDを取得しておく (以下参考)

https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds

```
$ aws configure

AWS Access Key ID [****************USKS]: <各自のAWSアクセスキーID>
AWS Secret Access Key [****************NLqd]: <各自のAWSシークレットキーID>
Default region name [ap-northeast-1]: ap-northeast-1
Default output format [text]: json

```

### SAMのセットアップ

```
$ cd src
```

#### ビルドの実行

```
$ sam build
```

#### デプロイ

```
$ sam deploy --guided

Stack Name [sam-app]: <任意のスタック名 または Enter>
AWS Region [ap-northeast-1]: ap-northeast-1
Confirm changes before deploy [y/N]: y
Allow SAM CLI IAM role creation [Y/n]: Y
Disable rollback [y/N]: y
AuthFunction may not have authorization defined, Is this okay? [y/N]: y
AuthCreateFunction may not have authorization defined, Is this okay? [y/N]: y
GetMyToDoFunction may not have authorization defined, Is this okay? [y/N]: y
CreateMyToDoFunction may not have authorization defined, Is this okay? [y/N]: y
UpdateMyToDoFunction may not have authorization defined, Is this okay? [y/N]: y
DeleteMyToDoFunction may not have authorization defined, Is this okay? [y/N]: y
SearchMyToDoFunction may not have authorization defined, Is this okay? [y/N]: y
Save arguments to configuration file [Y/n]: Y
SAM configuration file [samconfig.toml]: Enter
SAM configuration environment [default]: Enter

Deploy this changeset? [y/N]: y

```

## GUIアプリケーションのセットアップ

Macのターミナルから実行

RESTAPIの動作をWebアプリケーション(ToDo管理アプリ)から確認することも可能です

### 必要なモジュール類のインストール

事前にnode.jsとnpmのインストールが必要です

#### vueのインストール

`$ npm install -g @vue/cli`

#### node_modulesのインストール

`$ cd vueapp`

`$ npm install`

### ローカルサーバーでVueアプリを起動

__※ 事前に `vueapp/src/main.js`の`axios.defaults.baseURL`に、上記SAMでデプロイ後のAPIゲートウェイエンドポイントURLを指定する__

*`axios.defaults.baseURL="https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com"`*

```
$ cd vueapp
```

```
$ npm run serve
```

*_`http://localhost:8080/`_*でRESTAPIに対応したToDo管理アプリを使用することが可能です





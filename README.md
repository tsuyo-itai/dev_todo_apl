# dev_todo_apl

## セットアップ

Macのターミナルから実行

### 必要なモジュール類のインストール

`$ pip3 install aws-sam-cli moto pytest`


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

ビルドの実行

`$ sam build`

デプロイ

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
CreateFunction may not have authorization defined, Is this okay? [y/N]: y
DeleteFunction may not have authorization defined, Is this okay? [y/N]: y
Save arguments to configuration file [Y/n]: Y
SAM configuration file [samconfig.toml]: Enter
SAM configuration environment [default]: Enter

Deploy this changeset? [y/N]: y

```



# API仕様書

API仕様書はAPIBlueprintを使用して作成

参考URL

https://zenn.dev/dozo/articles/06fdbede4d5204

https://dev.classmethod.jp/articles/api-document-with-api-blueprint/

https://qiita.com/oskamathis/items/c374138635eb0012b119

## APIBlueprintの導入

Macのターミナルから実行

```
$ npm install
```

```
$ npm install -g aglio
```

## API仕様書の作成

`.apib`の拡張子でマークダウン記法ベースで作成 (ベースファイルはsrcに格納)

作成した`.apib`ファイルを`.html`形式へ出力

```
$ npx aglio -i Hoge.apib -o Hoge.html
```

一括でAPI仕様書を作成するためのshellを`bin`配下へ用意

```
$ ./bin/combine.sh
```

`output`フォルダへ出力されます

すべてのAPI仕様をまとめたファイル `ToDoAplAPI.html`



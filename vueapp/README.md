# vueapp

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
__※ 事前に `vueapp/src/main.js`の`axios.defaults.baseURL`に、上記SAMでデプロイ後のAPIゲートウェイエンドポイントURLを指定する__

*`axios.defaults.baseURL="https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com"`*

```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

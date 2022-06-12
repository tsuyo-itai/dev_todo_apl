<template>
  <div>
    <h1>ログイン画面</h1>
    <div>
      <input
        type="text"
        @keypress.enter="loginDataSend"
        v-model="LoginId"
        placeholder="ログインIDを入力"
      />
    </div>
    <div>
      <input
        type="text"
        @keypress.enter="loginDataSend"
        v-model="LoginPass"
        placeholder="ログインPASSを入力"
      />
    </div>
    <span class="error_msg">{{ ErrorMsg }}</span>
    <div>
      <button v-on:click="loginDataSend">Login</button>
    </div>
    <div>
      <router-link to="/auth/create">新規ユーザー登録はこちらから</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      LoginId: "",
      LoginPass: "",
      ErrorMsg: "",
    };
  },
  mounted() {
    this.LoginCheck();
  },
  methods: {
    LoginCheck() {
      // セッションストレージからログイントークンを取得する
      if (sessionStorage.getItem("login_token") != null) {
        this.$router.replace("todos");
      }
    },
    loginDataSend() {
      this.axios
        .post("/Prod/auth/", {
          login_id: this.LoginId,
          login_pass: this.LoginPass,
        })
        .then((response) => {
          console.log("【POST】API OK!!");
          // 認証成功時はログイントークンが返される
          console.log(response.data);
          let login_token = response.data.login_token;
          let login_id = response.data.login_id;
          sessionStorage.setItem("login_token", login_token);
          sessionStorage.setItem("login_id", login_id);
          this.$router.push("/todos");
        })
        .catch((error) => {
          console.log("【POST】API NG!!");
          console.log(error.response);
          this.ErrorMsg = error.response.data.message;
        });
      // テキストボックスのクリア
      this.LoginId = "";
      this.LoginPass = "";
    },
  },
};
</script>

<style scoped>
.error_msg {
  color: red;
}

h1 {
  color: #1e90ff;
}

input {
  margin: 7px;
}

button {
  margin: 7px;
}
</style>

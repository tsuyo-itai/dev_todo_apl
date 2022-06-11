<template>
  <div>
    <p>ログイン画面</p>
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
          let login_token = response.data.login_token;
          console.log(login_token);
          sessionStorage.setItem("login_token", login_token);
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
</style>

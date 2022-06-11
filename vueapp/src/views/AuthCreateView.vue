<template>
  <div>
    <p>ユーザー登録画面</p>
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
      <button v-on:click="loginDataSend">ユーザー作成</button>
    </div>
    <div>
      <router-link to="/auth">ログインはこちらから</router-link>
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
  methods: {
    loginDataSend() {
      this.axios
        .post("/Prod/auth/create", {
          login_id: this.LoginId,
          login_pass: this.LoginPass,
        })
        .then((response) => {
          console.log("【POST】API OK!!");
          console.log(response.data);
          this.$router.replace("auth");
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

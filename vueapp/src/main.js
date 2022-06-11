import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import VueAxios from "vue-axios";

const app = createApp(App);

// axios設定
axios.defaults.baseURL = "";

axios.defaults.headers.post["Content-Type"] = "application/json;charset=utf-8";

app.use(router);
app.use(VueAxios, axios);

app.mount("#app");

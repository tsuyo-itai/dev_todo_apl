<template>
  <div class="todolist_body">
    <h1>ToDOリスト一覧</h1>
    <div class="user-container">
      <h4>ようこそ {{ LoginId }} さん</h4>
      <button type="button" v-on:click="Logout">ログアウト</button>
    </div>

    <div class="todocontainer">
      <h3>タイトル</h3>
      <h3>内容</h3>
    </div>
    <template v-if="ActionType == 'Show'">
      <div
        class="todocontainer"
        v-for="(data, key) in TodoDatas"
        :key="key"
        v-bind:id="data.todo_id"
      >
        <span>{{ data.todo_title }}</span>
        <span>{{ data.todo_details }}</span>
        <button
          type="button"
          v-on:click="EditBtnClicked($event.currentTarget.parentElement.id)"
        >
          編集
        </button>
        <button
          type="button"
          v-on:click="DelBtnClicked($event.currentTarget.parentElement.id)"
        >
          削除
        </button>
      </div>
    </template>

    <template v-else-if="ActionType == 'Search'">
      <div
        class="todocontainer"
        v-for="(data, key) in SearchTodoDatas"
        :key="key"
        v-bind:id="data.todo_id"
      >
        <span>{{ data.todo_title }}</span>
        <span>{{ data.todo_details }}</span>
        <button
          type="button"
          v-on:click="EditBtnClicked($event.currentTarget.parentElement.id)"
        >
          編集
        </button>
        <button
          type="button"
          v-on:click="DelBtnClicked($event.currentTarget.parentElement.id)"
        >
          削除
        </button>
      </div>
    </template>

    <div v-else class="todocontainer" v-bind:id="EditData.todo_id">
      <input type="text" v-model="EditData.todo_title" />
      <input type="text" v-model="EditData.todo_details" />
      <button
        type="button"
        v-on:click="UpateToDo($event.currentTarget.parentElement.id)"
      >
        更新
      </button>
      <button
        type="button"
        v-on:click="DelBtnClicked($event.currentTarget.parentElement.id)"
      >
        削除
      </button>
    </div>
    <div>
      <input
        type="text"
        v-model="ToDoTitle"
        placeholder="ToDoのタイトルを入力"
      />
      <input type="text" v-model="ToDoDetails" placeholder="ToDoの内容を入力" />
    </div>
    <button type="button" v-on:click="AddToDo">ToDo追加</button>
    <div class="search-container">
      <input type="text" v-model="SearchWord" placeholder="検索ワード" />
      <button type="button" v-on:click="SearchToDo">検索</button>
      <button type="button" v-on:click="SearchToDoReset">検索リセット</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      LoginToken: "",
      LoginId: "",
      ToDoTitle: "",
      ToDoDetails: "",
      SearchWord: "",
      TodoDatas: [],
      SearchTodoDatas: [],
      ActionType: "Show",
      EditData: "",
    };
  },
  mounted() {
    this.LoginCheck();
  },
  methods: {
    LoginCheck() {
      // セッションストレージからログイントークンを取得する
      this.LoginToken = sessionStorage.getItem("login_token");
      this.LoginId = sessionStorage.getItem("login_id");
      console.log(this.LoginToken);
      if (this.LoginToken == null) {
        this.$router.replace("auth");
      } else {
        this.GetToDo();
      }
    },
    AddToDo() {
      this.ActionType = "Show";
      if (this.ToDoTitle !== "" && this.ToDoDetails !== "") {
        this.axios
          .post("/Prod/todos/create", {
            login_token: this.LoginToken,
            todo_title: this.ToDoTitle,
            todo_details: this.ToDoDetails,
          })
          .then((response) => {
            console.log("【POST】API OK!!");
            console.log(response.data);
            let addtodo = {
              todo_id: response.data.todo_id,
              todo_title: response.data.todo_title,
              todo_details: response.data.todo_details,
              login_token: response.data.login_token,
            };
            this.TodoDatas.push(addtodo);
            // this.$router.go({path: '/todos', force: true})
          })
          .catch((error) => {
            console.log("【POST】API NG!!");
            console.log(error.response);
          });
      } else {
        console.log("TODOが空のときの処理を追加");
      }
      // テキストボックスのクリア
      this.ToDoTitle = "";
      this.ToDoDetails = "";
    },
    DelToDo(todo_id) {
      // DELETEメソッドはdataに格納することでbodyに含め送信可能
      this.axios
        .delete("/Prod/todos/", {
          data: {
            todo_id: todo_id,
            login_token: this.LoginToken,
          },
        })
        .then((response) => {
          console.log("【POST】API OK!!");
          console.log(response.data);
          this.TodoDatas.forEach((TodoData, index) => {
            console.log(TodoData.todo_id);
            if (TodoData.todo_id == todo_id) {
              this.TodoDatas.splice(index, 1);
            }
          });
          this.SearchTodoDatas.forEach((SearchTodoData, index) => {
            console.log(SearchTodoData.todo_id);
            if (SearchTodoData.todo_id == todo_id) {
              this.SearchTodoDatas.splice(index, 1);
            }
          });
          this.EditData = "";
          if (this.ActionType == "Edit") {
            this.ActionType = "Show";
          }
          // this.$router.go({path: '/todos', force: true})
        })
        .catch((error) => {
          console.log("【POST】API NG!!");
          console.log(error.response);
        });
    },
    GetToDo() {
      this.axios
        .post("/Prod/todos", {
          login_token: this.LoginToken,
        })
        .then((response) => {
          console.log("【POST】API OK!!");
          this.TodoDatas = response.data.todos;
        })
        .catch((error) => {
          console.log("【POST】API NG!!");
          console.log(error.response);
        });
    },
    DelBtnClicked(todoid) {
      console.log(todoid);
      this.DelToDo(todoid);
    },
    SearchToDo() {
      this.axios
        .post("/Prod/todos/search", {
          login_token: this.LoginToken,
          search_word: this.SearchWord,
        })
        .then((response) => {
          console.log("【POST】API OK!!");
          console.log("SearchToDo");
          console.log(response.data);
          this.ActionType = "Search";
          console.log(typeof response.data);
          console.log(typeof response.data.todos);
          this.SearchTodoDatas = response.data.todos;
        })
        .catch((error) => {
          console.log("【POST】API NG!!");
          console.log(error.response);
        });
    },
    SearchToDoReset() {
      this.ActionType = "Show";
    },
    EditBtnClicked(todo_id) {
      console.log("EditBtnClicked");
      console.log(todo_id);
      this.TodoDatas.forEach((TodoData) => {
        if (TodoData.todo_id == todo_id) {
          console.log(TodoData);
          this.EditData = TodoData;
          this.ActionType = "Edit";
        }
      });
    },
    UpateToDo(todo_id) {
      // /Prod/todos
      console.log("UpateToDo");
      console.log(todo_id);
      this.ActionType = "Show";
      this.axios
        .put("/Prod/todos", {
          login_token: this.LoginToken,
          todo_id: todo_id,
          todo_title: this.EditData.todo_title,
          todo_details: this.EditData.todo_details,
        })
        .then((response) => {
          console.log("【POST】API OK!!");
          console.log(response);
          this.TodoDatas.forEach((TodoData, index) => {
            if (TodoData.todo_id == response.data.todo_id) {
              this.TodoDatas.splice(index, 1, response.data);
              this.ActionType = "Show";
            }
          });
        })
        .catch((error) => {
          console.log("【POST】API NG!!");
          console.log(error.response);
        });
    },
    Logout() {
      sessionStorage.clear();
      this.LoginToken = "";
      this.LoginId = "";
      this.LoginCheck();
    },
  },
};
</script>

<style scoped>
input {
  margin: 5px;
}

button {
  margin: 5px;
}

.user-container {
  display:flex;
  justify-content: center;
}

.user-container button {
  max-height: 35px;
  margin: auto 15px;
}

.todolist_body {
  width: 450px;
  margin: 0 auto auto auto;
}
.todocontainer-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.todocontainer {
  display: grid;
  grid-template-columns: 150px 150px 1fr 1fr;
  width: 100%;
  margin-bottom: 10px;
}

.search-container {
  margin: 20px;
}
</style>

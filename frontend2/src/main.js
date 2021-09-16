import { createApp } from "vue";
import { store } from "./store";
import { router } from "./router";
import "./index.css";

import App from "./App.vue";
import Field from "./components/ui/Field.vue";
import Button from "./components/ui/Button.vue";
import EditableList from "./components/ui/EditableList.vue";

const app = createApp(App);

app.use(router);
app.use(store);

// Global Components

// UI
app.component("Field", Field);
app.component("Button", Button);
app.component("EditableList", EditableList);

app.mount("#app");

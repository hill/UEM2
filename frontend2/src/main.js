import { createApp } from "vue";
import { store } from "./store";
import { router } from "./router";
import "./index.css";

import App from "./App.vue";
import Field from "./components/ui/Field.vue";

const app = createApp(App);

app.use(router);
app.use(store);

// Global Components
app.component("Field", Field);

app.mount("#app");

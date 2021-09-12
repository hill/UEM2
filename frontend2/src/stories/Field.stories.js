import Field from "../components/ui/Field.vue";

import { action } from "@storybook/addon-actions";

export default {
  component: Field,
  title: "Ui/Field",
};

const Template = (args) => ({
  components: { Field },
  setup() {},
});

export const Text = () => ({
  components: { Field },
  template: '<Field type="text" label="name" />',
});

import Field from "../components/ui/Field.vue";

import { action } from "@storybook/addon-actions";

export default {
  component: Field,
  title: "Ui/Field",
};

const Template = (args) => ({
  components: { Field },
  setup() {
    return { args };
  },
  template: '<Field v-bind="args" />',
});

export const Text = Template.bind({});
Text.args = { type: "text", label: "name" };
export const Password = Template.bind({});
Password.args = { type: "password", label: "password" };

import Button from "../components/ui/Button.vue";

import { action } from "@storybook/addon-actions";

export default {
  component: Button,
  title: "Ui/Button",
};

const Template = (args) => ({
  components: { Button },
  setup() {
    return { args };
  },
  template: '<Button v-bind="args" />',
});

export const Default = Template.bind({});
Default.args = { label: "Done" };

export const Primary = Template.bind({});
Primary.args = { label: "Done", style="primary" };
<script>
  import CourseCard from "../components/CourseCard.vue";
  import { AuthService, CourseService } from "../services/api.service";
  import { PaletteService } from "../services/palette.service";
  import { STRIPE_PUBLIC_KEY } from "../config";

  const blacklist = [
    "to",
    "the",
    "a",
    "and",
    "of",
    "or",
    "on",
    "introduction",
    "intro",
  ];
  const stripe = Stripe(STRIPE_PUBLIC_KEY);

  export default {
    components: { CourseCard },
    data() {
      return {
        courseNumber: null,
        courseName: null,
        due: null,
        primaryResource: null,
        syllabus: [
          //   { id: 1, name: "Introduction to Physics", complete: false },
        ],
        courseColor: "#222222",
        assessments: [
          // {name: "Demo", due: "some date", weight: 50.0, complete: false},
        ],
        motivators: {
          payOnFail: {
            active: false,
            price: 0,
          },
          refundOnSuccess: false,
          tweet: false,
          tweetFromAccount: false,
          exposeSecret: false,
        },
        showPaymentModal: false,
        elements: null,
      };
    },
    mounted() {
      this.rollCourse();
    },
    methods: {
      addAssessment() {
        this.assessments.push({
          name: "",
          due: null,
          weight: 0,
          complete: false,
        });
      },
      rollCourse() {
        this.courseNumber = Math.floor(Math.random() * (999 - 100 + 1) + 100);
        this.courseColor = PaletteService.chooseRandomColor();
      },
      async save() {
        const courseCode = this.initials + String(this.courseNumber);
        try {
          const response = await CourseService.create(
            this.courseName,
            courseCode,
            null,
            this.primaryResource,
            this.due,
            this.syllabus,
            this.assessments,
            "completing",
            this.courseColor
          );
          this.$router.push("/transcript");
        } catch (err) {
          console.log(err);
        }
      },
      async setupPayment() {
        this.showPaymentModal = true;
        try {
          const response = await AuthService.getSetupIntentSecret();
          const { client_secret: clientSecret } = response.data;
          const options = {
            clientSecret,
          };
          this.elements = stripe.elements(options);

          const paymentElement = this.elements.create("payment");
          paymentElement.mount("#payment-element");
        } catch (err) {
          console.error(err);
        }
      },
      async submitPaymentDetails(event) {
        event.preventDefault();

        const { error, setupIntent } = await stripe.confirmSetup({
          elements: this.elements,
          confirmParams: {
            return_url: "http://localhost:3000/setup-complete",
          },
          redirect: "if_required",
        });

        if (error) {
          // TODO: display stripe errors nicely
        } else {
          console.log(setupIntent);
          this.showPaymentModal = false;
        }
      },
    },
    computed: {
      initials() {
        let words = this.courseName?.split(" ") ?? [];
        words = words.filter((word) => !blacklist.includes(word.toLowerCase()));

        if (words.length == 0) {
          return "UEM";
        }

        if (words.length == 1) {
          return words[0]
            .substring(0, Math.min(4, words[0].length))
            .toUpperCase();
        }

        const courseName = words.map((word) => word[0]?.toUpperCase()).join("");
        return courseName
          .substring(0, Math.min(4, courseName.length))
          .toUpperCase();
      },
    },
  };
</script>
<template>
  <div class="page px-2 md:px-10 lg:px-20 py-10 min-h-screen">
    <div
      class="bg-gray-50 block shadow-xl sm:flex flex-row-reverse p-5 rounded-2xl min-h-screen"
    >
      <div class="cover flex-1 relative">
        <div class="sm:w-1/2 sm:fixed p-10">
          <CourseCard
            class="mx-auto w-3/4 md:1/2 lg:w-2/5 xl:w-1/3"
            :code="initials + courseNumber"
            :name="courseName"
            :color="courseColor"
          />
          <div class="mt-5 mx-auto text-center">
            <Button label="Roll" @click="rollCourse()" />
          </div>
        </div>
      </div>
      <div class="form flex-1 space-y-8">
        <section>
          <h1 class="text-xl font-extrabold">New Course</h1>
          <div class="space-y-8 p-4">
            <Field
              label="Course Name"
              v-model="courseName"
              autocomplete="off"
            />
            <Field label="Due" type="date" v-model="due" autocomplete="off" />
            <Field
              label="Primary Resource"
              type="text"
              v-model="primaryResource"
              autocomplete="off"
            />
          </div>
        </section>
        <section>
          <h1 class="text-xl font-extrabold">Syllabus</h1>
          <div class="p-4">
            <EditableList v-model="syllabus" />
          </div>
        </section>
        <section>
          <h1 class="text-xl font-extrabold">Assessment</h1>
          <div class="p-4">
            <div
              v-for="assessment in assessments"
              class="rounded-lg p-2 my-3 border-2 border-gray-400 shadow-lg space-y-4"
            >
              <Field label="Name" v-model="assessment.name" />
              <div class="flex">
                <Field
                  class="flex-1"
                  label="Due"
                  type="date"
                  v-model="assessment.due"
                  autocomplete="off"
                />
                <Field
                  class="flex-1 ml-4"
                  label="Weight"
                  type="number"
                  v-model="assessment.weight"
                />
              </div>
            </div>
            <Button @click="addAssessment()" label="Add Assessment" />
          </div>
        </section>
        <section>
          <h1 class="text-xl font-extrabold">Motivators</h1>
          <div class="p-4 space-y-2">
            <Checkbox
              v-model="motivators.payOnFail.active"
              label="Pay on failure"
            />
            <div
              v-if="motivators.payOnFail.active"
              class="rounded-md p-3 bg-gray-200 space-y-3"
            >
              <h3 class="text-md">Pay On Failure</h3>
              <p class="text-sm">
                If a mark > 50% is not achieved by the due date {{ due }}, we
                will charge your card ${{ motivators.payOnFail.price }}.00
              </p>
              <input
                class="w-3/4"
                id="price"
                type="range"
                min="0"
                max="1000"
                step="5"
                v-model="motivators.payOnFail.price"
              />
              <label class="ml-1" for="price"
                >${{ motivators.payOnFail.price }}.00</label
              >
              <Button
                class="block"
                label="Set Up Payment"
                @click="setupPayment()"
              />
              <Modal v-model="showPaymentModal">
                <div class="bg-white rounded-lg p-2 space-y-3">
                  <form id="payment-form">
                    <div id="payment-element">
                      <!-- Elements will create form elements here -->
                      Loading...
                    </div>
                    <Button label="submit" @click="submitPaymentDetails" />
                    <div id="error-message">
                      <!-- Display error message to your customers here -->
                    </div>
                  </form>
                </div>
              </Modal>
            </div>
            <Checkbox
              v-model="motivators.refundOnSuccess"
              label="Pay now; Refund on success"
            />
            <Checkbox v-model="motivators.tweet" label="Tweet failure" />
            <Checkbox
              v-model="motivators.tweetFromAccount"
              label="Tweet failure from my account"
            />
            <Checkbox
              v-model="motivators.exposeSecret"
              label="Expose deep secret"
            />
          </div>
        </section>
        <div class="text-center">
          <Button @click="save()" label="Create" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .page {
    background-color: #cdd2d8;
  }
</style>

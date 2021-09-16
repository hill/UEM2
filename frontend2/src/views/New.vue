<script>
  import CourseCard from "../components/CourseCard.vue";
  import { CourseService } from "../services/api.service";
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
      };
    },
    mounted() {
      this.generateCourseNumber();
    },
    methods: {
      generateCourseNumber() {
        this.courseNumber = Math.floor(Math.random() * (999 - 100 + 1) + 100);
      },
      save() {
        const courseCode = this.initials + String(this.courseNumber);
        CourseService.create(
          this.courseName,
          courseCode,
          "",
          this.due,
          this.syllabus,
          "completing"
        )
          .then((res) => {
            this.$router.push("/transcript");
          })
          .catch((err) => {
            console.log(err.response);
          });
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
      class="bg-gray-50 block sm:flex flex-row-reverse p-5 rounded-2xl min-h-screen"
    >
      <div class="cover flex-1 relative">
        <div class="sm:w-1/2 sm:fixed p-10">
          <CourseCard
            class="mx-auto w-3/4 md:1/2 lg:w-2/5 xl:w-1/3"
            :code="initials + courseNumber"
            :name="courseName"
          />
          <div class="mt-5 mx-auto text-center">
            <Button label="Roll" @click="generateCourseNumber()" />
          </div>
        </div>
      </div>
      <div class="form flex-1">
        <h1 class="text-xl font-extrabold">New Course</h1>
        <div class="space-y-8 p-4">
          <Field label="Course Name" v-model="courseName" />
          <Field label="Due" type="date" v-model="due" />
          <Field
            label="Primary Resource"
            type="text"
            v-model="primaryResource"
          />
        </div>
        <h1 class="text-xl font-extrabold">Syllabus</h1>
        <div class="p-4">
          <EditableList v-model="syllabus" />
        </div>
        <h1 class="text-xl font-extrabold">Assessment</h1>
        <h1 class="text-xl font-extrabold">Motivators</h1>
        <div class="text-center">
          <Button @click="save()" label="Create" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .page {
    background-color: #b2b2b2; /* TODO(TOM): add to pallette */
  }
</style>

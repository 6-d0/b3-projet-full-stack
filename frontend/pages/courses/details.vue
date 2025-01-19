<template>
  <Navbar />
  <div class="container">
    <h1 class="text-3xl font-semibold text-left text-gray-800 m-4 p-5">
      Mes cours
    </h1>
    <div class="p-5">
      <div
        v-for="course in courses"
        :key="course.uuid"
        class="bg-gray-50 p-4 m-3 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
      >
        <div class="text-xl font-semibold text-gray-900">
          {{ course.name }}
        </div>
        <div class="text-gray-600">
          Professeur : {{ course.teacher.last_name }}
          {{ course.teacher.first_name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  setup() {
    const courses = ref<ICourses[] | null>(null);
    const fetchCourses = async (teacher_uuid: string) => {
      const { data: acourses } = await useAPI<ICourses[]>(
        `/courses/${teacher_uuid}/courses/`
      );
      if (acourses.value) {
        courses.value = acourses.value;
      }
    };

    onMounted(() => {
      const teacher_uuid = userStore().user?.uuid as string;
      fetchCourses(teacher_uuid);
    });
    return {
      courses,
    };
  },
};
</script>

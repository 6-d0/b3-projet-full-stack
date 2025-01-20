<template>
  <Navbar />
  <div class="container">
    <div class="">
      <h1 class="font-bold text-2xl mb-6">{{ session?.name }}</h1>
    </div>
    <div class="" v-for="course in courses">
      <div
        class="my-6 flex justify-between items-center p-4 bg-white border border-gray-200 rounded-lg shadow-lg hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 transition-all"
      >
        {{ course.name }}
        <button
          v-if="
            session?.courses?.some(
              (sessionCourse) => sessionCourse.slug === course.slug
            )
          "
          @click="
            () => {
              deleteFromSession(course.uuid);
            }
          "
          class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
        >
          Supprimer
        </button>
        <button
          class="text-white bg-green-600 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
          v-else
          @click="
            () => {
              addOnSession(course.uuid);
            }
          "
        >
          Ajouter
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
export default {
  setup() {
    const courses = ref<ICourses[] | null>(null);
    const session = ref<ISession>();
    const fetchSession = async (slug: string) => {
      const { data: asession } = await useAPI<ISession[]>(`/sessions/`);
      if (asession.value) {
        session.value =
          asession.value.find((s) => s.slug === slug) || undefined;
      }
    };
    const fetchMyCourses = async () => {
      const { data: acourses } = await useAPI<ICourses[]>(
        `/courses/${userStore().user?.uuid}/courses/`
      );
      if (acourses.value) {
        courses.value = acourses.value;
      }
    };

    const deleteFromSession = async (uuid: string) => {
      const response = await useAPI(`/sessions/${session_slug}/courses/`, {
        method: "DELETE",
        body: { uuid: uuid },
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": `${userStore().token}`,
        },
        credentials: "include",
      });
    };

    const addOnSession = async (uuid: string) => {
      const response = await useAPI(`/sessions/${session_slug}/courses/`, {
        method: "PATCH",
        body: { uuid: uuid },
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": `${userStore().token}`,
        },
        credentials: "include",
      });
    };
    const route = useRoute();
    const session_slug = route.params.session_slug as string;
    onMounted(() => {
      fetchMyCourses();
      fetchSession(session_slug);
    });
    return {
      courses,
      session,
      deleteFromSession,
      addOnSession,
      session_slug,
    };
  },
};
</script>

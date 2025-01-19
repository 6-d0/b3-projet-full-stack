<template>
  <Navbar />
  <div class="container mx-auto p-6 max-w-4xl">
    <div
      v-if="registration"
      class="p-6 bg-white rounded-lg shadow-md border border-gray-200 dark:bg-gray-800 dark:border-gray-700"
    >
      <h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-4">
        Détails de l'inscription
      </h2>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Cours :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ registration.course.name }}
        </p>
      </div>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Date de la prise de rendez-vous :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ new Date(registration.date).toLocaleDateString() }}
        </p>
      </div>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Heures :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ formatTime(registration.slot.begin_time) }} -
          {{ formatTime(registration.slot.end_time) }}
        </p>
      </div>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Local :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ registration.slot.schedule.classroom }}
        </p>
      </div>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Étudiant :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ registration.student.last_name.toUpperCase() }}
          {{ registration.student.first_name }}
          (<a
            :href="`mailto:${registration.student.email}`"
            class="text-blue-500 hover:underline"
          >
            {{ registration.student.email }} </a
          >)
        </p>
      </div>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Commentaire :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ registration.comment }}
        </p>
      </div>

      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Date du rendez-vous :
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          {{ new Date(registration.slot.schedule.date).toLocaleDateString() }}
        </p>
      </div>
    </div>

    <div
      v-else
      class="flex items-center justify-center h-48 text-gray-500 dark:text-gray-400"
    >
      Chargement...
    </div>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";

export default {
  setup() {
    const route = useRoute();
    const registration = ref<IRegistration | null>(null);

    function formatTime(d: Date) {
      const date = new Date(d);
      let hours = date.getHours();
      let minutes = date.getMinutes();
      const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
      return `${lzero(hours)}:${lzero(minutes)}`;
    }

    const fetchRegistration = async (uuid: string) => {
      const { data: r } = useAPI<IRegistration>(
        `/registrations/${uuid}/details/`
      );
      registration.value = r.value;
    };
    onMounted(() => {
      const uuid = route.params.slot_uuid as string;
      fetchRegistration(uuid);
    });

    return {
      registration,
      fetchRegistration,
      formatTime,
    };
  },
};
</script>

<template>
  <Navbar />
  <div class="container mx-auto px-4 py-12">
    <h1
      class="text-3xl font-bold text-gray-800 dark:text-white mb-8 text-center"
    >
      Mes Inscriptions
    </h1>
    <ul
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
    >
      <li
        v-for="registration in registrations"
        :key="registration.uuid"
        class="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-md overflow-hidden transition-transform transform hover:scale-105"
      >
        <NuxtLink
          :to="`/timeslots/my-timeslots/${registration.uuid}/`"
          class="block p-6 space-y-4 h-full"
        >
          <h5
            class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white truncate"
          >
            {{ registration.course.name }}
          </h5>

          <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
            <p>
              {{ registration.slot.schedule.teacher.last_name.toUpperCase() }}
              {{ registration.slot.schedule.teacher.first_name }}
              <span class="text-xs text-gray-500">
                ({{ registration.slot.schedule.classroom || "Pas de local" }})
              </span>
            </p>
          </div>

          <div
            class="mt-4 flex flex-col items-start text-sm text-gray-800 dark:text-gray-200 space-y-1"
          >
            <span class="font-medium">
              {{ formatTime(registration.slot.begin_time) }} -
              {{ formatTime(registration.slot.end_time) }}
            </span>
            <span class="text-xs text-gray-500">
              {{
                new Date(registration.slot.schedule.date).toLocaleDateString()
              }}
            </span>
          </div>
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

const route = useRoute();
import { userStore } from "~/stores/user";
import authGlobal from "~/middleware/auth.global";
import Navbar from "~/components/ui/navbar/Navbar.vue";

export default {
  setup() {
    definePageMeta({
      middleware: authGlobal,
      roles: ["student"],
    });
    const user = userStore().user;
    const registrations = ref<IRegistration[] | null>(null);
    const fetchRegistrations = async () => {
      const { data: aregistrations } = await useAPI<IRegistration[] | null>(
        "/registrations/my-registrations"
      );
      if (aregistrations.value) registrations.value = aregistrations.value;
    };

    onMounted(async () => {
      fetchRegistrations();
    });

    function formatTime(d: any) {
      const date = new Date(d);
      let hours = date.getHours();
      let minutes = date.getMinutes();
      const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
      return `${lzero(hours)}:${lzero(minutes)}`;
    }

    return {
      user,
      registrations,
      formatTime,
    };
  },
};
</script>

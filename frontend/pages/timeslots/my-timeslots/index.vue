<template>
  <Navbar />
  <div class="container mx-auto px-4 py-12">
    <ul
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
    >
      <li
        v-for="registration in registrations"
        class="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-md overflow-hidden"
      >
        <NuxtLink :to="`${registration.uuid}`">
          <div class="p-6 space-y-4 h-52">
            <div class="flex justify-between items-center h-1/3">
              <h5
                class="text-base sm:text-lg md:text-xl lg:text-2xl font-semibold text-gray-900 dark:text-white"
              >
                {{ registration.course.name }}
              </h5>
            </div>

            <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
              <p>
                {{ registration.slot.schedule.teacher.last_name.toUpperCase() }}
                {{ registration.slot.schedule.teacher.first_name }}
                ({{ registration.slot.schedule.classroom }})
              </p>
            </div>

            <div
              class="mt-4 flex items-center justify-between text-sm text-gray-800 dark:text-gray-200"
            >
              <span class="font-medium">
                {{ formatTime(registration.slot.begin_time) }} -
                {{ formatTime(registration.slot.end_time) }}
              </span>
            </div>
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

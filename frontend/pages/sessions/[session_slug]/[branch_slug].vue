<template>
  <Navbar />
  <div class="container mx-auto p-6">
    <h2 class="text-2xl font-bold text-center">
      {{ session?.name }}
    </h2>

    <ul class="mb-6">
      <li
        :key="branch?.uuid"
        class="text-lg font-semibold text-gray-800 dark:text-gray-200"
      >
        <h1 class="text-black-600">
          {{ branch?.name }}
        </h1>
      </li>
    </ul>

    <div
      v-if="loading"
      class="text-center text-xl text-gray-500 dark:text-gray-400 mb-6"
    >
      Chargement des horaires...
    </div>

    <ul
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
    >
      <li
        v-for="schedule in schedules.filter(
          (s) => s.teacher.username === user?.username
        )"
        v-if="user?.role === 'teacher'"
        :key="schedule.uuid"
        class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
      >
        <NuxtLink :href="`/timeslots/${schedule.uuid}/`">
          <div class="flex row justify-between">
            <h5
              class="mb-2 text-2xl font-semibold text-gray-900 dark:text-white"
            >
              {{ schedule.teacher.last_name.toUpperCase() }}
              {{ schedule.teacher.first_name }}
            </h5>
          </div>
          <h6 class="mb-4 text-l font-small text-gray-800 dark:text-gray-300">
            {{ schedule.teacher.email }}
          </h6>
          <p class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3">
            {{ schedule.classroom }}
          </p>
          <div class="space-x-4">
            <span
              v-if="schedule.can_subscribe"
              class="text-center w-fit px-2 py-1 bg-green-600 text-white font-semibold rounded-lg shadow-md"
            >
              Inscription active {{ schedule.can_subscribe_until }}
            </span>
            <span
              v-else
              class="text-center w-fit px-2 py-1 bg-red-600 text-white font-semibold rounded-lg shadow-md"
            >
              Inscription inactive
            </span>
          </div>
        </NuxtLink>
        <div
          @click="() => deleteSchedule(schedule.uuid)"
          class="cursor-pointer"
        >
          x
        </div>
      </li>
      <li
        v-if="user?.role === 'teacher'"
        class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 ease-in-out dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
      >
        <NuxtLink :href="`/schedules/`">
          <div class="flex flex-col items-center justify-center h-full">
            <div class="flex items-center justify-center p-0 rounded-full">
              <h5 class="text-3xl font-semibold">+</h5>
            </div>
            <p
              class="text-lg font-medium text-gray-900 dark:text-white text-center"
            >
              Ajouter un créneau
            </p>
          </div>
        </NuxtLink>
      </li>

      <!-- afficher les schedules avec des timeslots pour les etudiants -->
      <li
        v-for="schedule in schedules.filter(
          (s) => hasTimeSlot(s.uuid) && s.can_subscribe
        )"
        v-else
        class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
      >
        <NuxtLink :href="`/timeslots/${schedule.uuid}/`">
          <h5 class="mb-2 text-2xl font-semibold text-gray-900 dark:text-white">
            {{ schedule.teacher.last_name.toUpperCase() }}
            {{ schedule.teacher.first_name }}
          </h5>
          <h6 class="mb-4 text-l font-small text-gray-800 dark:text-gray-300">
            {{ schedule.teacher.email }}
          </h6>
          <p class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3">
            {{ schedule.classroom }}
          </p>
          <div>
            <span
              v-if="schedule.can_subscribe"
              class="text-center w-fit px-2 py-1 bg-green-600 text-white font-semibold rounded-lg shadow-md"
            >
              Inscription active {{ schedule.can_subscribe_until }}
            </span>
            <span
              v-else
              class="text-center w-fit px-2 py-1 bg-red-600 text-white font-semibold rounded-lg shadow-md"
            >
              Inscription inactive
            </span>
          </div>
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

// par rapport au nom des fichiers
const route = useRoute();
const session_slug = route.params.session_slug as string;
const branch_slug = route.params.branch_slug as string;
const scheduleTimeslots = ref<{ [uuid: string]: ITimeslots[] }>({});

// pour utiliser dans la page
const session = ref<ISession | null>(null);
const branch = ref<IBranch | null>(null);
var schedules = ref<ISchedules[]>([]);
const loading = ref<boolean>(true);

// recuperer user
import { userStore } from "~/stores/user";
import Navbar from "~/components/ui/navbar/Navbar.vue";
const user = userStore().user;

/**
 * Retrouve une branche selon son slug
 * @param slug le slug de la branche
 */
async function fetchBranches(slug: string) {
  try {
    const { data: abranches } = await useAPI<IBranch[]>(
      `/branches/${route.params.session_slug}`
    );
    branch.value = abranches.value?.find((b) => b.slug === slug) || null;
  } catch (error) {
    console.error(error);
  }
}

/**
 * Retrouve une session a partir d'un slug
 * @param slug le slug de la session
 */
async function fetchSession(slug: string) {
  try {
    const { data: asession } = await useAPI<ISession[]>(`/sessions/`);
    session.value = asession.value?.find((s) => s.slug === slug) || null;
  } catch (error) {
    console.error(error);
  }
}

/**
 * Retrouve les schedules liés à une branche
 * @param branch_slug le slug d'une branche
 * @param session_slug le slug d'une session
 */
async function fetchSchedules(branch_slug: string, session_slug: string) {
  try {
    const response = await fetch(
      `http://localhost:9000/api/v1/schedules/${session_slug}/${branch_slug}`
    );
    if (!response.ok) {
      throw new Error("Error while fetching schedules");
    }
    const data = await response.json();
    schedules.value = data;
    for (const schedule of data) {
      const responseTimeslot = await fetch(
        `http://localhost:9000/api/v1/timeslots/${schedule.uuid}`
      );
      if (responseTimeslot.ok) {
        const timeslotData = await responseTimeslot.json();
        scheduleTimeslots.value[schedule.uuid] = timeslotData;
      }
    }
  } catch (error) {
    console.error("Erreur:", error);
  } finally {
    loading.value = false;
  }
}

function hasTimeSlot(uuid: string): boolean {
  return (
    scheduleTimeslots.value[uuid] && scheduleTimeslots.value[uuid].length > 0
  );
}

const deleteSchedule = async (uuid: string) => {
  const token = userStore().token;
  const response = await useAPI(`/schedules/delete/${uuid}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": `${token}`,
    },
    credentials: "include",
  });
  schedules.value = schedules.value.filter((s) => s.uuid !== uuid);
};

onMounted(() => {
  fetchSession(session_slug);
  fetchBranches(branch_slug);
  fetchSchedules(branch_slug, session_slug);
});
</script>

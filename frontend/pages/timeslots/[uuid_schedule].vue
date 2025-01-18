<template>
  <Navbar />
  <div class="container mx-auto p-6 bg-gray-50">
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-6">
      {{ teacher?.last_name }} {{ teacher?.first_name }}
    </h2>

    <ul class="space-y-4">
      <li
        v-for="timeslot in timeslots"
        :key="`${timeslot.uuid}`"
        class="flex justify-between items-center p-4 bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300"
      >
        <span class="text-lg font-semibold text-gray-900">
          {{ formatTime(timeslot.begin_time) }} -
          {{ formatTime(timeslot.end_time) }}
        </span>
        <NuxtLink
          :to="`/timeslots/register/${schedule_slug}/${timeslot.uuid}`"
          v-if="canSubscribe"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
        >
          Register
        </NuxtLink>
        <NuxtLink
          :to="`/timeslots/details/${timeslot.uuid}`"
          v-if="user?.role === 'teacher'"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
        >
          Details
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

const route = useRoute();
var timeslots = ref<ITimeslots[] | null>(null);
const schedule_slug = route.params.uuid_schedule.toString();
var teacher = ref<IUser | null>(null);
var canSubscribe = ref(false);

// recup user
import { userStore } from "~/stores/user";
const user = userStore().user;

/**
 * récupère les timeslots d'un schedule, si c'est un professeur, recupère tout, sinon, seulement ceux disponibles
 * @param s_slug le slug du schedule
 */
const fetchTimeSlots = async (s_slug: string) => {
  try {
    const { data: atimeslot } = await useAPI<ITimeslots[]>(
      `/timeslots/${s_slug}/${user?.role === "student" ? "available" : ""}`
    );
    if (atimeslot?.value) {
      timeslots.value = atimeslot.value.sort((s, t) => {
        const startS = new Date(s.begin_time).getTime();
        const startT = new Date(t.begin_time).getTime();
        return startS - startT;
      });
      console.log(...timeslots.value);

      const teacher_from_schedule = timeslots.value[0]?.schedule.teacher;
      if (teacher_from_schedule) {
        teacher.value = teacher_from_schedule;
      }

      if (teacher.value && user?.username !== teacher.value.username) {
        if (user?.role === "teacher") {
          navigateTo("/unauthorized");
        } else {
          canSubscribe.value = true;
        }
      }
    }
  } catch (error) {
    console.error("Error fetching timeslots:", error);
  }
};

/**
 * Formate la date au format HH:mm
 * @param dateString la date a formatter
 */
const formatTime = (dateString: string | Date) => {
  const date = new Date(dateString);
  console.log(dateString);
  console.log(date);
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
};

onMounted(() => {
  fetchTimeSlots(schedule_slug);
});
</script>

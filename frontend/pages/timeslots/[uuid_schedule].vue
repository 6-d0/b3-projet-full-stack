<template>
  <div class="container mx-auto p-6 bg-gray-50">
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-6">
      {{ teacher?.last_name }} {{ teacher?.first_name }}
    </h2>

    <ul class="space-y-4">
      <li
        v-for="timeslot in timeslots"
        class="flex justify-between items-center p-4 bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300"
      >
        <span class="text-lg font-semibold text-gray-900">
          {{ formatTime(timeslot.begin_time) }} -
          {{ formatTime(timeslot.end_time) }}
        </span>
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

// recup user
import { userStore } from "~/stores/user";
const user = userStore().user;

/**
 * récupère les timeslots d'un schedule
 * @param s_slug le slug du schedule
 */
const fetchTimeSlots = async (s_slug: string) => {
  const { data: atimeslot } = await useAPI<ITimeslots[]>(
    `/timeslots/${s_slug}`
  );
  timeslots.value = atimeslot.value;

  if (timeslots.value && timeslots.value.length > 0) {
    const teacher_from_schedule = timeslots.value.at(0)?.schedule.teacher; // récupère le nom du prof (pour affichage)
    if (teacher_from_schedule) {
      teacher.value = teacher_from_schedule;
    }
  }

  if (teacher.value && user?.username !== teacher.value.username) {
    navigateTo("/unauthorized");
  }
};

/**
 * Formate la date au format HH:mm
 * @param dateString la date a formatter
 */
const formatTime = (dateString: Date) => {
  const date = new Date(dateString);
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
};

onMounted(() => {
  fetchTimeSlots(schedule_slug);
});
</script>

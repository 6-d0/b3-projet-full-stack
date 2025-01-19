<template>
  <Navbar />
  <div class="container mx-auto p-6 bg-gray-50">
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-6">
      {{ teacher?.last_name }} {{ teacher?.first_name }}
    </h2>

    <table class="min-w-full table-auto mx-auto">
      <thead>
        <tr class="bg-gray-100 text-gray-900">
          <th class="px-6 py-3 text-center">Time Slot</th>
          <th class="px-6 py-3 text-center" v-if="user?.role === 'student'">
            Register
          </th>
          <th class="px-6 py-3 text-center" v-else>Details</th>
          <th class="px-6 py-3 text-center" v-if="user?.role === 'teacher'">
            Inscription
          </th>
        </tr>
      </thead>
      <tbody class="text-center">
        <tr
          v-for="timeslot in timeslots"
          :key="`${timeslot.uuid}`"
          class="border-b border-gray-200"
        >
          <td class="px-6 py-4">
            <span class="text-lg font-semibold text-gray-900">
              {{ formatTime(timeslot.begin_time) }} -
              {{ formatTime(timeslot.end_time) }}
            </span>
          </td>
          <td class="px-6 py-4">
            <NuxtLink
              :to="`/timeslots/register/${schedule_slug}/${timeslot.uuid}`"
              v-if="canSubscribe"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
            >
              Register
            </NuxtLink>
            <NuxtLink
            v-if="user?.role === 'teacher' && isRegistration(timeslot.uuid)"
            :to="`/timeslots/${timeslot.uuid}/details`"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
            >
              Details
            </NuxtLink>
            <button
              disabled
              v-if="user?.role === 'teacher' && !isRegistration(timeslot.uuid)"
              class="cursor-default disabled bg-gray-500 text-white font-bold py-2 px-4 rounded-full"
            >
              Details
        </button>
          </td>
          <td>
            <span v-if="isRegistration(timeslot.uuid)">
              {{ isRegistration(timeslot.uuid).student.first_name }}
              {{ isRegistration(timeslot.uuid).student.last_name }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { ref } from "vue";
import Navbar from "~/components/ui/navbar/Navbar.vue";

const route = useRoute();

const schedule_slug = route.params.uuid_schedule.toString();
var teacher = ref<IUser | null>(null);
var canSubscribe = ref(false);

// recup user
import { userStore } from "~/stores/user";
const user = userStore().user;

//pour les timeslots et les registrations
var timeslots = ref<ITimeslots[] | null>(null);
var registrations = ref<any[]>([]);

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

      const { data: registrationsData } = await useAPI<any[]>(
        `/registrations/${s_slug}/`
      );
      if (registrationsData?.value) {
        registrations.value = registrationsData.value;
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
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
};

/**
 * Get the registration for a specific slot
 * @param slotUuid the uuid of the slot
 */
const isRegistration = (slotUuid: string | null): IRegistration => {
  return registrations.value.find(
    (registration) => registration.slot.uuid === slotUuid
  );
};
onMounted(() => {
  fetchTimeSlots(schedule_slug);
});
</script>

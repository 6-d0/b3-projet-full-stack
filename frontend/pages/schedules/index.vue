<script setup lang="ts">
import Toaster from "@/components/ui/toast/Toaster.vue";
import { Input } from "@/components/ui/input";
import { reactive, ref, computed, watch } from "vue";
import { formatDate } from "@vueuse/core";
import authGlobal from "~/middleware/auth.global";
definePageMeta({
  middleware: authGlobal,
  roles: ["teacher"],
});
const token = userStore().token;

const date = new Date("2025-01-01");
const canSubscribe = ref<Boolean | null>(false);
const startTime = ref("08:00");
const rangeTime = ref(15);
const endTime = ref("09:00");
const pauseTime = ref(0);

interface ITimeSlot {
  id: number;
  value: string;
  end: string;
  editing: boolean;
}

function formatTime(d: Date) {
  let hours = d.getHours();
  let minutes = d.getMinutes();
  const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
  return `${lzero(hours)}:${lzero(minutes)}`;
}

const timeslots = ref<ITimeSlot[]>([
  {
    id: 1,
    value: formatTime(new Date("2025-01-01 8:00")),
    end: formatTime(new Date("2025-01-01 8:15")),
    editing: false,
  },
  {
    id: 2,
    value: formatTime(new Date("2025-01-01 8:15")),
    end: formatTime(new Date("2025-01-01 8:30")),
    editing: false,
  },
  {
    id: 3,
    value: formatTime(new Date("2025-01-01 8:30")),
    end: formatTime(new Date("2025-01-01 8:45")),
    editing: false,
  },
  {
    id: 4,
    value: formatTime(new Date("2025-01-01 8:45")),
    end: formatTime(new Date("2025-01-01 9:00")),
    editing: false,
  },
]);

const timeslotsSorted = computed(() =>
  [...timeslots.value].sort((a, b) => a.value.localeCompare(b.value))
);

let idCounter = 0;

function generateSlots() {
  const startDate = new Date(date);
  const endDate = new Date(date);
  const [startTimeHour, startTimeMinute]: Array<number> = startTime.value
    .split(":")
    .map((e) => parseInt(e));
  const [endTimeHour, endTimeMinute]: Array<number> = endTime.value
    .split(":")
    .map((e) => parseInt(e));

  startDate.setMinutes(startTimeMinute);
  startDate.setHours(startTimeHour);

  endDate.setMinutes(endTimeMinute);
  endDate.setHours(endTimeHour);

  const times: Array<{ start: string; end: string }> = [];

  while (startDate < endDate) {
    const endTime = new Date(startDate);
    endTime.setMinutes(startDate.getMinutes() + rangeTime.value);

    times.push({
      start: formatTime(startDate),
      end: formatTime(endTime),
    });

    startDate.setMinutes(
      startDate.getMinutes() + rangeTime.value + pauseTime.value
    );
  }

  timeslots.value.splice(0, timeslots.value.length);
  for (const { start, end } of times) {
    timeslots.value.push({
      id: idCounter++,
      value: start,
      end,
      editing: false,
    });
  }
}

const sessions = ref<ISession[] | null>(null);
const fetchSession = async () => {
  const { data: asession } = await useAPI<ISession[] | null>(`/sessions/`);
  sessions.value = asession.value;
};
const local = ref<string>("");
const can_subscribe_until = ref<Date | null>(null);
const saveSchedule = async (): Promise<number | undefined> => {
  if (selectedDate.value && new Date(selectedDate.value) < new Date()) {
    alert("impossible de créer un schedule a une date qui est déjà passée");
    return;
  }
  const data = {
    date: selectedDate.value,
    can_subscribe: canSubscribe.value,
    session: selectedSession,
    classroom: local.value ?? null,
    can_subscribe_until: can_subscribe_until.value
      ? `${can_subscribe_until.value}`
      : null,
  };

  const response = await useAPI<ISchedules>("/schedules/create-schedule/", {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": `${token}`,
    },
    credentials: "include",
  });
  return response.data.value?.pk;
};

const saveTimeslots = async (pk: number) => {
  const start = new Date();
  const end = new Date();
  const start_hour = parseInt(startTime.value.split(":")[0], 10);
  const start_min = parseInt(startTime.value.split(":")[1], 10);
  const end_hour = parseInt(endTime.value.split(":")[0], 10);
  const end_min = parseInt(endTime.value.split(":")[1], 10);
  start.setHours(start_hour);
  start.setMinutes(start_min);
  end.setHours(end_hour);
  end.setMinutes(end_min);
  const data = {
    schedule_id: pk,
    start_time: `${start.toISOString()}`,
    end_time: `${end.toISOString()}`,
    duration: `${rangeTime.value}`,
    break_duration: `${pauseTime.value}`,
  };
  const response = await useAPI<ITimeSlot[]>("/timeslots/create/", {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": `${token}`,
    },
    credentials: "include",
  });
};
const save = async () => {
  const pk = await saveSchedule();
  if (pk) {
    saveTimeslots(pk);
    return navigateTo(`my-schedules/`);
  }
};

/**
 * formatte la date d'auj
 */
function formatTodayDate(): string {
  const today = new Date();

  const year = today.getFullYear();
  const month = (today.getMonth() + 1).toString().padStart(2, "0");
  const day = today.getDate().toString().padStart(2, "0");

  return `${year}-${month}-${day}`;
}

watch([startTime, endTime, pauseTime, rangeTime], () => {
  generateSlots();
});

const selectedSession = ref<ISession>();
const selectedDate = ref<Date>();

fetchSession();
</script>

<template>
  <Navbar />
  <Toaster />

  <form
    class="container bg-white max-w-[40vw] mx-auto p-8 rounded-lg shadow-xl"
    @submit.prevent="save"
  >
    <div class="space-y-6">
      <div class="flex flex-col">
        <label for="session" class="text-sm font-semibold text-gray-700 mb-2">
          Session:
        </label>
        <div class="relative">
          <select
            name="session"
            id="session"
            autocomplete="session-name"
            v-model="selectedSession"
            class="block w-full appearance-none rounded-md border border-gray-300 bg-white py-2 px-3 text-base text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
            required
          >
            <option
              class="text-base"
              v-for="session in sessions"
              :value="session.pk"
              :key="session.pk"
            >
              {{ session.name }}
            </option>
          </select>
          <svg
            class="pointer-events-none absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 w-5 h-5"
            fill="currentColor"
            viewBox="0 0 16 16"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M4.22 6.22a.75.75 0 0 1 1.06 0L8 8.94l2.72-2.72a.75.75 0 1 1 1.06 1.06l-3.25 3.25a.75.75 0 0 1-1.06 0L4.22 7.28a.75.75 0 0 1 0-1.06Z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
      </div>

      <div class="flex flex-col">
        <label for="session" class="text-sm font-semibold text-gray-700 mb-2">
          Date:
        </label>
        <input
          type="date"
          v-model="selectedDate"
          class="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-base text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
          required
          :min="formatTodayDate()"
        />
      </div>

      <div class="grid grid-cols-2 align-middle space-x-2 w-full">
        <div class="flex mx-6 w-fit pb-3">
          <label
            for="can-subscribe"
            class="text-sm text-center align-middle justify-center font-semibold text-gray-700 mb-4 pb-2"
          >
            Peut s'inscrire:
          </label>
          <input
            type="checkbox"
            v-model="canSubscribe"
            class="block rounded-md border align-middle justify-center mx-6 my-1 h-min border-gray-300 bg-white py-2 px-3 text-base text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
          />
          <div v-if="canSubscribe">
            <input
              type="date"
              :max="`${selectedDate}`"
              :min="formatTodayDate()"
              value=""
              v-model="can_subscribe_until"
            />
          </div>
        </div>
        <div class="mx-auto center">
          <label
            for="local"
            class="text-sm text-center font-semibold text-gray-700 mb-2"
            >Local</label
          >
          <input
            type="text"
            placeholder="Local"
            v-model="local"
            class="bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
      </div>

      <div class="flex flex-col">
        <label
          for="start-time"
          class="text-sm font-semibold text-gray-700 mb-2"
        >
          Début:
        </label>
        <input
          id="start-time"
          v-model="startTime"
          type="time"
          class="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
        />
      </div>

      <div class="flex flex-col">
        <label
          for="pause-time"
          class="text-sm font-semibold text-gray-700 mb-2"
        >
          Pause (minutes):
        </label>
        <input
          id="pause-time"
          v-model="pauseTime"
          type="number"
          min="0"
          class="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
        />
      </div>

      <div class="flex flex-col">
        <label
          for="range-time"
          class="text-sm font-semibold text-gray-700 mb-2"
        >
          Range (minutes):
        </label>
        <input
          id="range-time"
          v-model="rangeTime"
          type="number"
          min="1"
          class="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
        />
      </div>

      <div class="flex flex-col">
        <label for="end-time" class="text-sm font-semibold text-gray-700 mb-2">
          Fin:
        </label>
        <input
          id="end-time"
          v-model="endTime"
          :min="endTime"
          type="time"
          class="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
        />
      </div>

      <div
        class="flex flex-col justify-start overflow-y-auto space-y-4 p-4 bg-gray-50 rounded-lg shadow-lg max-h-[40vh]"
      >
        <div
          class="flex items-center justify-between bg-white rounded-md p-4 shadow-sm border border-gray-200 hover:shadow-lg transition-shadow"
          v-for="timeslot in timeslotsSorted"
          :key="timeslot.id"
        >
          <div class="flex items-center justify-center space-x-4 w-full">
            <input
              v-model="timeslot.value"
              class="h-12 w-full max-w-[300px] rounded-md border border-gray-300 bg-gray-50 px-4 py-2 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              type="time"
              :disabled="!timeslot.editing"
            />

            <input
              class="h-12 w-full max-w-[300px] rounded-md border border-gray-300 bg-gray-50 px-4 py-2 text-sm text-gray-500"
              type="time"
              :value="timeslot.end"
              :disabled="true"
            />
          </div>
        </div>
      </div>

      <button
        type="submit"
        class="w-full bg-blue-500 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-md transition duration-300"
      >
        Créer
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import Toaster from "@/components/ui/toast/Toaster.vue";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast/use-toast";
import { reactive, ref, computed, watch } from "vue";
import { Pencil, Save } from "lucide-vue-next";
import Navbar from "~/components/ui/navbar/Navbar.vue";

const { toast } = useToast();
const inputRefs: { [index: number]: HTMLInputElement } = {};
const token = userStore().token;

const date = new Date("2025-01-01");
const canSubscribe = ref<Boolean | null>(false);
const startTime = ref("09:00");
const rangeTime = ref(15);
const endTime = ref("12:00");
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

const saveSchedule = async (): Promise<number | undefined> => {
  const data = {
    date: selectedDate.value,
    can_subscribe: canSubscribe,
    session: selectedSession,
    classroom: `B4`,
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
  console.log(response.data.value?.teacher);
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
  console.log(response.data.value);
  console.log(response.error.value);
  console.log(data);
};
const save = async (): Promise<void> => {
  const pk = await saveSchedule();
  if (pk) {
    console.log(pk);
    saveTimeslots(pk);
  } else {
    console.log("Erreur : Le schedule n'a pas pu être créé.");
  }
};

watch([startTime, endTime, pauseTime, rangeTime], () => {
  generateSlots();
});

const selectedSession = ref<ISession>();
const selectedDate = ref<Date>();
onMounted(() => {
  fetchSession();
});
</script>

<template>
  <Navbar />
  <Toaster />

  <form
    class="container bg-gray-50 max-w-[40vw] mx-auto p-6 rounded-lg shadow-md"
    @submit.prevent="save"
  >
    <div class="space-y-6">
      <div class="flex flex-col">
        <label for="session" class="text-sm font-medium text-gray-700 mb-2">
          Session:
        </label>
        <select name="session" id="session" v-model="selectedSession" required>
          <option
            v-for="session in sessions"
            :value="session.pk"
            :key="session.pk"
            selected
          >
            {{ session.name }}
          </option>
        </select>
      </div>

      <div class="flex flex-col">
        <label for="session" class="text-sm font-medium text-gray-700 mb-2">
          Date:
        </label>
        <input type="date" v-model="selectedDate" required />
      </div>

      <div class="flex flex-col">
        <label for="session" class="text-sm font-medium text-gray-700 mb-2">
          Can Subscribe:
        </label>
        <input type="checkbox" v-model="canSubscribe" />
      </div>

      <div class="flex flex-col">
        <label for="start-time" class="text-sm font-medium text-gray-700 mb-2">
          Début:
        </label>
        <Input
          id="start-time"
          v-model="startTime"
          type="time"
          class="h-10 w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
        />
      </div>

      <div class="flex flex-col">
        <label for="pause-time" class="text-sm font-medium text-gray-700 mb-2">
          Pause (minutes):
        </label>
        <Input
          id="pause-time"
          v-model="pauseTime"
          type="number"
          min="0"
          class="h-10 w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
        />
      </div>

      <div class="flex flex-col">
        <label for="range-time" class="text-sm font-medium text-gray-700 mb-2">
          Range (minutes):
        </label>
        <Input
          id="range-time"
          v-model="rangeTime"
          type="number"
          min="1"
          class="h-10 w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
        />
      </div>

      <div class="flex flex-col">
        <label for="end-time" class="text-sm font-medium text-gray-700 mb-2">
          Fin:
        </label>
        <Input
          id="end-time"
          v-model="endTime"
          type="time"
          class="h-10 w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
        />
      </div>
    </div>

    <div
      class="flex flex-col justify-center center overflow-y-auto space-y-4 p-4 bg-gray-100 rounded-lg shadow-md max-h-[60vh] w-[40vw] mx-auto my-4 py-5"
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
            class="h-12 w-full max-w-[300px] rounded-md border border-gray-300 bg-gray-50 px-4 py-2 text-sm text-gray-500 cursor-not-allowed"
            type="time"
            :value="timeslot.end"
            :disabled="true"
          />
        </div>
      </div>
    </div>

    <button
      type="submit"
      class="mx-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
    >
      Créer
    </button>
  </form>
</template>

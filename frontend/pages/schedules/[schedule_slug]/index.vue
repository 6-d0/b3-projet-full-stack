<script setup lang="ts">
import Toaster from "@/components/ui/toast/Toaster.vue";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast/use-toast";
import { reactive, ref, computed, watch } from "vue";
import { Pencil, Save } from "lucide-vue-next";

const { toast } = useToast();
const inputRefs: { [index: number]: HTMLInputElement } = {};

// par rapport au nom des fichiers
const route = useRoute();
const schedule_slug = route.params.schedule_slug as string;

const date = new Date("2025-01-01");
const startTime = ref("09:00");
const rangeTime = ref(15);
const endTime = ref("12:00");
const pauseTime = ref(0);
var timeslotsSorted = ref<ITimeslots[] | null>(null);
var timeslots = ref<ITimeslots[] | null>(null);

function formatTime(d: Date) {
  let hours = d.getHours();
  let minutes = d.getMinutes();
  const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
  return `${lzero(hours)}:${lzero(minutes)}`;
}

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

  timeslots.value?.splice(0, timeslots.value?.length);
  for (const [i, { start, end }] of times.entries()) {
    if(schedule.value)
    timeslots.value?.push({schedule: schedule.value, begin_time: startDate, end_time: endDate, uuid:null});
  }
  console.log(timeslots);
}

var schedule = ref<ISchedules | null>(null)
const fetchSchedules = async (uuid: string) => {
  const {data: aschedules}  = await useAPI<ISchedules[]>(
    `/schedules/teacher-schedules/`
  )
  const response = ref<ISchedules | undefined>(aschedules.value?.filter((s) => s.uuid === uuid).at(0));
  if(response.value){
    schedule.value = response.value
  }
}

onMounted(() => {
  fetchSchedules(schedule_slug);
});

</script>

<template>
  <Toaster />
  <h1>Schedule de {{ schedule?.teacher }}</h1>

  <form class="container" @submit.prevent="generateSlots()">
    <div class="max-w-md mx-auto py-3">
      <label
        >Début:
        <Input v-model="startTime" type="time"/>
      </label>

      <label
        >Pause (minutes):
        <Input v-model="pauseTime" type="number" />
      </label>

      <label
        >Range (minutes)
        <Input v-model="rangeTime" type="number" min="1" />
      </label>

      <label
        >Fin
        <Input v-model="endTime" type="time" />
      </label>

      <input
        class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
        type="submit"
        value="Envoyer"
      />
    </div>
  </form>

  
  <div class="flex flex-col justify-center">
    <div
      class="flex justify-center items-center"
      v-for="timeslot in timeslotsSorted"
    >
      <div class="flex items-center space-x-2">
        <input
          class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          type="time"
        />
        <input
          class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          type="time"
          :value="timeslot.end_time"
          :disabled="true"
        />
      </div>
    </div>
  </div>
</template>

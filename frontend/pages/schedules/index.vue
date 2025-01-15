<script setup lang="ts">
import Toaster from "@/components/ui/toast/Toaster.vue";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast/use-toast";
import { reactive, ref, computed, watch } from "vue";
import { Pencil, Save } from "lucide-vue-next";

const { toast } = useToast();
const inputRefs: { [index: number]: HTMLInputElement } = {};

const date = new Date("2025-01-01");

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

const timeslots: Array<ITimeSlot> = reactive([
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
  [...timeslots].sort((a, b) => a.value.localeCompare(b.value))
);

const globalEditing = ref(false);
function changeTimeSlot(id: number) {
  const timeslot: ITimeSlot | undefined = timeslots.find((ts) => ts.id == id);
  if (!timeslot) {
    globalEditing.value = false;
    return;
  }

  const newStartTime = inputRefs[id].value;
  const [newStartHour, newStartMinute] = newStartTime
    .split(":")
    .map((e) => parseInt(e));
  const newStartDate = new Date();
  newStartDate.setHours(newStartHour);
  newStartDate.setMinutes(newStartMinute);

  const newEndDate = new Date(newStartDate);
  newEndDate.setMinutes(newStartDate.getMinutes() + rangeTime.value);

  const isOverlapping = timeslots.some((ts) => {
    if (ts.id === id) return false;
    const [existingStartHour, existingStartMinute] = ts.value
      .split(":")
      .map((e) => parseInt(e));
    const existingStartDate = new Date();
    existingStartDate.setHours(existingStartHour);
    existingStartDate.setMinutes(existingStartMinute);

    const existingEndDate = new Date(existingStartDate);
    existingEndDate.setMinutes(
      existingStartDate.getMinutes() + rangeTime.value
    );

    return (
      (newStartDate < existingEndDate && newEndDate > existingStartDate) ||
      (existingStartDate < newEndDate && existingEndDate > newStartDate)
    );
  });

  if (isOverlapping) {
    toast({
      title: "Les créneaux horaires se chevauchent",
      variant: "destructive",
    });
  } else {
    timeslot.value = newStartTime;
    timeslot.end = formatTime(newEndDate);
  }

  timeslot.editing = false;
  globalEditing.value = false;
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

  timeslots.splice(0, timeslots.length);
  for (const [i, { start, end }] of times.entries()) {
    timeslots.push({ id: i, value: start, end, editing: false });
  }
  console.log(timeslots);
}
</script>

<template>
  <Toaster />

  <form class="container" @submit.prevent="generateSlots()">
    <div class="max-w-md mx-auto py-3">
      <label
        >Début:
        <Input v-model="startTime" type="time" />
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
      :key="timeslot.id"
    >
      <div class="flex items-center space-x-2">
        <input
          class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          type="time"
          :value="timeslot.value"
          :disabled="!timeslot.editing"
          @keyup.enter="changeTimeSlot(timeslot.id)"
          :ref="el => inputRefs[timeslot.id] = el as HTMLInputElement"
        />
        <input
          class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          type="time"
          :value="timeslot.end"
          :disabled="true"
        />
      </div>
      <Button
        class="p-1"
        variant="outline"
        v-if="!timeslot.editing"
        :disabled="globalEditing"
        @click="
          globalEditing = true;
          timeslot.editing = true;
        "
      >
        <Pencil />
      </Button>
      <Button
        class="p-1"
        variant="outline"
        v-show="timeslot.editing"
        @click="changeTimeSlot(timeslot.id)"
      >
        <Save />
      </Button>
    </div>
  </div>
</template>

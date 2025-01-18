<template>
  <Navbar />
  <div v-if="slot" class="p-6 max-w-lg mx-auto bg-white rounded-lg shadow-lg">
    <div class="text-center mb-4">
      <h2 class="text-2xl font-semibold text-gray-800">
        {{ formatTime(new Date(slot.begin_time)) }} -
        {{ formatTime(new Date(slot.end_time)) }}
      </h2>
    </div>

    <form
      action=""
      method="post"
      @submit.prevent="saveRegistration"
      class="space-y-6"
    >
      <div class="flex flex-col">
        <label for="comment" class="text-gray-700 font-medium mb-2"
          >Commentaire</label
        >
        <input
          type="text"
          v-model="comment"
          name="comment"
          id="comment"
          class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Laissez un commentaire"
        />
      </div>

      <div class="flex flex-col">
        <label for="courses" class="text-gray-700 font-medium mb-2"
          >Choisir un cours</label
        >
        <select
          v-model="courseSelect"
          name="courses"
          id="courses"
          class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option
            v-for="course in courses"
            :value="course.slug"
            :key="course.slug"
          >
            {{ course.name }}
          </option>
        </select>
      </div>

      <div class="flex justify-center">
        <input
          type="submit"
          value="S'inscrire"
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full transition-all duration-300"
        />
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";
import authGlobal from "~/middleware/auth.global";

// recuperer user
import { userStore } from "~/stores/user";

export default {
  setup() {
    definePageMeta({
      middleware: authGlobal,
      roles: ["student"],
    });
    const route = useRoute();
    const slot_uuid = route.params.slot_uuid as string;
    const schedule_uuid = route.params.schedule_uuid as string;
    const user = userStore().user;
    const token = userStore().token;

    const slot = ref<ITimeslots | null>(null);
    const schedule = ref<ISchedules | null>(null);
    const courses = ref<ICourses[] | null>(null);
    const comment = ref("");
    const courseSelect = ref<ICourses | null>(null);

    const fetchTimeSlots = async (uuid: string) => {
      try {
        const { data: aslots } = await useAPI<ITimeslots[] | null>(
          `/timeslots/${uuid}/`
        );
        if (aslots?.value) {
          slot.value = aslots.value.filter((ts) => ts.uuid === slot_uuid)[0];
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des créneaux : ", error);
      }
    };

    const fetchSchedules = async (uuid: string) => {
      const { data: aschedule } = await useAPI<ISchedules | null>(
        `/schedules/${schedule_uuid}`
      );
      schedule.value = aschedule.value;
    };

    function formatTime(d: Date) {
      let hours = d.getHours();
      let minutes = d.getMinutes();
      const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
      return `${lzero(hours)}:${lzero(minutes)}`;
    }

    const fetchCourses = async (uuid: string) => {
      const { data: acourses } = await useAPI<ICourses[] | null>(
        `/courses/${uuid}/courses`
      );
      courses.value = acourses.value;
    };

    const saveRegistration = async () => {
      if (!courseSelect.value) {
        console.error("Veuillez remplir tous les champs");
        return;
      }

      const data = {
        course: courseSelect.value,
        timeslot: slot_uuid,
        comment: comment.value,
      };

      try {
        const token = userStore().token;

        const response = await useAPI("/registrations/add/", {
          method: "POST",
          body: data,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": `${token}`,
          },
          credentials: "include",
        });
        console.log(response.status.value);
        if (response.status.value === "success") {
          return navigateTo("/timeslots/my-timeslots/");
        } else {
          alert(
            `Erreur: ${
              response.error
                ? response.error.value?.data.non_field_errors
                : "Cause inconnue"
            }`
          );
        }
      } catch (error) {
        console.error("Erreur lors de l'enregistrement", error);
      }
    };

    onMounted(async () => {
      await fetchTimeSlots(schedule_uuid);
      await fetchSchedules(schedule_uuid);
      if (schedule.value) {
        const teacher_uuid = schedule.value.teacher.uuid;
        await fetchCourses(teacher_uuid);
      } else {
      }
    });

    return {
      slot,
      schedule,
      courses,
      user,
      comment,
      courseSelect,
      formatTime,
      saveRegistration,
      definePageMeta,
    };
  },
};
</script>

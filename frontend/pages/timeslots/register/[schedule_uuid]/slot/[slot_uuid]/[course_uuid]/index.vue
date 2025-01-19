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
        <label for="comment" class="text-gray-700 font-medium mb-2">
          Commentaire
        </label>
        <input
          type="text"
          v-model="comment"
          name="comment"
          id="comment"
          class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Laissez un commentaire"
        />
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

  <Modal
    v-if="showModal"
    :visible="showModal"
    :title="modalTitle"
    @close="showModal = false"
  >
    <p>{{ modalMessage }}</p>
  </Modal>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";
import Modal from "~/components/ui/modal/Modal.vue";
import authGlobal from "~/middleware/auth.global";

// recuperer user
import { userStore } from "~/stores/user";

export default {
  components: {
    Modal,
  },
  setup() {
    definePageMeta({
      middleware: authGlobal,
      roles: ["student"],
    });
    const route = useRoute();
    const slot_uuid = route.params.slot_uuid as string;
    const schedule_uuid = route.params.schedule_uuid as string;
    const user = userStore().user;

    const slot = ref<ITimeslots | null>(null);
    const schedule = ref<ISchedules | null>(null);
    const courses = ref<ICourses | null>(null);
    const comment = ref("");
    const courseSelect = ref<ICourses | null>(null);

    // modals vars
    const showModal = ref(false);
    const modalTitle = ref("");
    const modalMessage = ref("");

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
        `/schedules/${schedule_uuid}/`
      );
      schedule.value = aschedule.value;
    };

    function formatTime(d: Date) {
      let hours = d.getHours();
      let minutes = d.getMinutes();
      const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
      return `${lzero(hours)}:${lzero(minutes)}`;
    }

    const fetchCourse = async (uuid: string, course_uuid: string) => {
      const { data: acourses } = await useAPI<ICourses[] | null>(
        `/courses/${uuid}/courses/`
      );
      if (acourses.value)
        courses.value = acourses.value
          .filter((s) => s.uuid === course_uuid)
          .at(0) as ICourses;
      console.log(courses.value);
    };

    const saveRegistration = async () => {
      const data = {
        course: `${courses.value?.slug}`,
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
        if (response.status.value === "success") {
          return navigateTo("/timeslots/my-timeslots/");
        } else {
          modalTitle.value = "Erreur d'inscription";
          modalMessage.value = response.error
            ? response.error.value?.data.non_field_errors[0]
            : "Cause inconnue";
          showModal.value = true;
        }
      } catch (error) {
        modalTitle.value = "Erreur";
        modalMessage.value = "Erreur lors de l'enregistrement";
        showModal.value = true;
      }
    };

    onMounted(async () => {
      await fetchTimeSlots(schedule_uuid);
      await fetchSchedules(schedule_uuid);
      if (schedule.value) {
        const teacher_uuid = schedule.value.teacher.uuid;
        const course_uuid = useRoute().params.course_uuid as string;
        await fetchCourse(teacher_uuid, course_uuid);
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
      showModal,
      modalTitle,
      modalMessage,
    };
  },
};
</script>

<template>
  <!-- modals -->
  <div
    id="popup-modal"
    tabindex="-1"
    v-show="isModalOpen"
    class="overflow-y-auto overflow-x-hidden fixed top-0 left-1/2 transform -translate-x-1/2 -translate-y-4 z-50 w-full max-w-md"
  >
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <button
          @click="closeModal"
          type="button"
          class="absolute top-3 end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
        >
          <svg
            class="w-3 h-3"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 14 14"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
            />
          </svg>
          <span class="sr-only">Close modal</span>
        </button>
        <div class="p-4 md:p-5 text-center">
          <svg
            class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 20"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Voulez-vous vraiment supprimer ce schedule?
          </h3>
          <button
            @click="() => deleteSchedule(selectedScheduleUuid)"
            data-modal-hide="popup-modal"
            type="button"
            class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
          >
            Yes, I'm sure
          </button>
          <button
            @click="closeModal"
            type="button"
            class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
          >
            No, cancel
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- page -->
  <Navbar />
  <div class="container mx-auto p-6">
    <h2 class="text-2xl font-semibold text-center">
      {{ session?.name }} - {{ branch?.name }}
    </h2>

    <div class="mb-6 text-lg font-semibold text-gray-800 dark:text-gray-200">
      Vue par professeur
    </div>

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
        v-if="userStore().isTeacher()"
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
          <div class="h-6 mb-2">
            <p
              class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3"
            >
              {{ schedule.classroom }}
            </p>
          </div>
          <div class="h-6 mb-2">
            <p
              class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3"
            >
              {{ new Date(schedule.date).toLocaleDateString() }}
            </p>
          </div>
        </NuxtLink>
        <div class="flex justify-between items-center space-x-4">
          <button
            @click="
              () => {
                changeCanSubscribe(schedule.pk, schedule.can_subscribe);
                schedule.can_subscribe = !schedule.can_subscribe;
              }
            "
            class="space-x-4 cursor-pointer"
          >
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
          </button>

          <button
            @click="() => openModal(schedule.uuid)"
            data-modal-target="popup-modal"
            data-schedule="`${schedule.uuid}`"
            class="inline-flex items-center justify-center p-1 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow-md transition-all duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800"
            type="button"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18 18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </li>
      <li
        v-if="userStore().isTeacher()"
        class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
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

      <!-- schedule avec timeslots uniquement (finalement non tous les schedules)-->
      <li
        v-for="schedule in schedules.filter(
          (s) => s.can_subscribe && new Date(s.date) > new Date()
        )"
        v-if="userStore().isStudent() || userStore().isAdmin()"
        class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
      >
        <NuxtLink :to="`/timeslots/${schedule.uuid}/`">
          <h5 class="mb-2 text-2xl font-semibold text-gray-900 dark:text-white">
            {{ schedule.teacher.last_name.toUpperCase() }}
            {{ schedule.teacher.first_name }}
          </h5>
          <h6 class="mb-2 text-l font-small text-gray-800 dark:text-gray-300">
            {{ schedule.teacher.email }}
          </h6>
          <div class="h-6 mb-2">
            <p class="text-sm font-normal text-gray-700 dark:text-gray-400">
              {{ schedule.classroom }}
            </p>
          </div>
          <div class="h-6 mb-2">
            <p
              class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3"
            >
              {{ new Date(schedule.date).toLocaleDateString() }}
            </p>
          </div>
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

    <div class="" v-if="userStore().isStudent()">
      <div
        :key="branch?.uuid"
        class="mt-10 mb-6 text-lg font-semibold text-gray-800 dark:text-gray-200"
      >
        <h1 class="text-black-600">Vue par cours</h1>
      </div>
      <div
        class="w-full mb-6 py-2"
        v-for="scheduleCourse in courses.filter(
          (c) => c.schedule?.session.slug === session_slug
        )"
      >
        <div class="flex items-center">
          <span class="text-s my-2 font-semibold">
            {{
              scheduleCourse.schedule
                ? new Date(
                    scheduleCourse.schedule?.date.toString()
                  ).toLocaleDateString()
                : ""
            }}
            -
            {{ scheduleCourse.schedule?.teacher.last_name }}
            {{ scheduleCourse.schedule?.teacher.first_name }}
          </span>
        </div>
        <ul
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
        >
          <li
            class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
            v-for="course in scheduleCourse.course"
          >
            <NuxtLink
              :to="`/timeslots/${scheduleCourse.schedule?.uuid}/${course.uuid}/`"
            >
              <h5
                class="mb-2 h-[30%] text-xl font-semibold text-gray-900 dark:text-white flex items-center"
              >
                <span class="my-auto">
                  {{ course.name }}
                </span>
              </h5>
              <h6
                class="mb-2 text-l font-small text-gray-800 dark:text-gray-300"
              >
                {{ scheduleCourse.schedule?.teacher.last_name }}
                {{ scheduleCourse.schedule?.teacher.first_name }}
              </h6>
              <div class="h-6 mb-2">
                <p class="text-sm font-normal text-gray-700 dark:text-gray-400">
                  {{ scheduleCourse.schedule?.classroom }}
                </p>
              </div>
              <div class="h-6 mb-2">
                <p
                  class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3"
                >
                  {{
                    scheduleCourse.schedule
                      ? new Date(
                          scheduleCourse.schedule.date
                        ).toLocaleDateString()
                      : ""
                  }}
                </p>
              </div>
              <div>
                <span
                  v-if="scheduleCourse.schedule?.can_subscribe"
                  class="text-center w-fit px-2 py-1 bg-green-600 text-white font-semibold rounded-lg shadow-md"
                >
                  Inscription active
                  {{ scheduleCourse.schedule?.can_subscribe_until }}
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { ref } from "vue";

// par rapport au nom des fichiers
const route = useRoute();
const session_slug = route.params.session_slug as string;
const branch_slug = route.params.branch_slug as string;
const scheduleTimeslots = ref<ITimeslots[]>([]);

// pour utiliser dans la page
const session = ref<ISession | null>(null);
const branch = ref<IBranch | null>(null);
const schedules = ref<ISchedules[]>([]);
const loading = ref<boolean>(true);
const token = userStore().token;
const isModalOpen = ref(false);
const selectedScheduleUuid = ref<string>();

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
    const { data: abranches } = await useAPI<IBranch[]>(`/branches/`);
    branch.value = abranches.value?.find((b) => b.slug === slug) || null;
  } catch (error) {
    console.error(error);
  }
}
class CourseSchedule {
  schedule: ISchedules | null;
  course: ICourses[];

  constructor(schedule: ISchedules | null, course: ICourses[]) {
    this.schedule = schedule;
    this.course = course;
  }
}

const courses = ref<CourseSchedule[]>([]);
const fetchCourses = async (uuid: string, schedule: ISchedules) => {
  try {
    if (schedule.can_subscribe) {
      const { data: acourses } = await useAPI<ICourses[] | undefined>(
        `/courses/${uuid}/${branch_slug}`
      );

      if (acourses?.value && Array.isArray(acourses.value)) {
        const filteredCourses = acourses.value.filter((course) => {
          return (
            session.value?.courses &&
            session.value.courses.filter((c) => c.uuid === course.uuid).length >
              0
          );
        });

        console.log(filteredCourses, "Filtered Courses");

        if (filteredCourses.length > 0) {
          courses.value.push(new CourseSchedule(schedule, filteredCourses));
        }
      }
    }
  } catch (error) {
    console.error(
      `Erreur lors de la récupération des cours pour le schedule ${uuid}:`,
      error
    );
  }
};

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
const fetchSchedules = async (branchSlug: string, sessionSlug: string) => {
  try {
    const response = await fetch(
      `/api/v1/schedules/${sessionSlug}/${branchSlug}`
    );
    if (!response.ok)
      throw new Error("Erreur lors de la récupération des schedules");

    const data = await response.json();
    schedules.value = data;

    // les profs ont pas besoin de voir leurs schedules par cours
    if (user?.role === "student") {
      await Promise.all(
        schedules.value.map(async (s) => {
          if (s) {
            await fetchCourses(s.teacher.uuid, s);
          }
        })
      );
    }

    const timeslotPromises = data.map(async (schedule: ISchedules) => {
      const { data: itimeslot } = await useAPI<ITimeslots>(
        `/api/v1/timeslots/${schedule.uuid}/available/`
      );
      if (itimeslot.value) {
        scheduleTimeslots.value.push(itimeslot.value);
      }
    });

    await Promise.all(timeslotPromises);
  } catch (error) {
    console.error("Erreur :", error);
  } finally {
    loading.value = false;
  }
};

/** ouais mais ca marche plus
 * Vérifie si le schedule a des timeslots
 * @param uuid l'uuid du schedule
 */
function hasTimeSlot(uuid: string): boolean {
  return scheduleTimeslots.value.length > 0;
}

/**
 * Supprime le schedule d'uuid uuid
 * @param uuid l'uuid du schedule a supprimer
 */
const deleteSchedule = async (uuid: string | undefined) => {
  const response = await useAPI(`/schedules/delete/${uuid}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": `${token}`,
    },
    credentials: "include",
  });
  schedules.value = schedules.value.filter((s) => s.uuid !== uuid);
  closeModal();
};

/**
 *
 * @param id l'id du schedule
 * @param current la valeur courante de canSubscribe
 */
const changeCanSubscribe = async (id: number, current: boolean) => {
  const data = {
    canSubscribe: current ? false : true,
  };
  const response = await useAPI(`/schedules/update-can-subscribe/${id}/`, {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": `${token}`,
    },
    credentials: "include",
  });
};
/**
 * Affiche le modal avant de supprimer
 * @param uuid l'uuid du schedule
 */
const openModal = (uuid: string) => {
  selectedScheduleUuid.value = uuid;
  isModalOpen.value = true;
};

/**
 * Ferme le modal
 */
const closeModal = () => {
  isModalOpen.value = false;
};

fetchSession(session_slug);
fetchBranches(branch_slug);
fetchSchedules(branch_slug, session_slug);
</script>

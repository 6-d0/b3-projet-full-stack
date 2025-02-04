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
  <div
    class="p-6 w-[75vw] mx-auto"
    v-for="(session, index) in sessions"
    :key="index"
  >
    <h1 class="text-pretty text-base font-semibold">{{ session.name }}</h1>
    <ul class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <li
        v-if="schedules"
        v-for="schedule in sortedSchedules(session)"
        :key="schedule.uuid"
        class="p-6 bg-white border border-gray-200 rounded-lg shadow-lg h-full hover:shadow-xl transition-shadow dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
      >
        <NuxtLink :to="`/timeslots/${schedule.uuid}/`">
          <h5 class="mb-2 text-2xl font-semibold text-gray-900 dark:text-white">
            {{ schedule.session.name }}
          </h5>
          <p class="mb-4 text-gray-700 dark:text-gray-300 text-sm">
            {{ new Date(schedule.date).toLocaleDateString() }}
          </p>
          <div class="h-6">
            <p
              v-if="schedule.classroom"
              class="text-sm font-normal text-gray-700 dark:text-gray-400 my-3"
            >
              Local: {{ schedule.classroom }}
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
            class="flex items-center justify-between mt-4 relative bottom-0"
          >
            <span
              v-if="schedule.can_subscribe"
              class="px-3 py-1 bg-green-600 text-white font-semibold rounded-lg shadow-md"
            >
              Inscription active
              {{
                schedule.can_subscribe_until
                  ? `(${new Date(
                      schedule.can_subscribe_until
                    ).toLocaleDateString()})`
                  : ""
              }}
            </span>
            <span
              v-else
              class="px-3 py-1 bg-red-600 text-white font-semibold rounded-lg shadow-md"
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
    </ul>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";

export default {
  setup() {
    const selectedScheduleUuid = ref<string>();
    const isModalOpen = ref<boolean>(false);
    const sessions = ref<ISessions>([]);
    const schedules = ref<ISchedules[] | null>(null);

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

    const fetchSchedules = async () => {
      try {
        const { data: schedules_data } = await useAPI<ISchedules[] | null>(
          "/schedules/teacher-schedules"
        );
        schedules.value = schedules_data?.value || [];

        if (schedules.value) {
          schedules.value.forEach((s) => {
            if (
              sessions.value.filter(
                (session) => session.slug === s.session.slug
              ).length === 0
            ) {
              sessions.value.push(s.session);
            }
          });
        }
      } catch (error) {
        console.error("Erreur:", error);
      }
    };

    const sortedSchedules = (session: ISession) => {
      if (!schedules.value) return [];
      return schedules.value
        .filter((s) => s.session.slug === session.slug)
        .sort((s1, s2) => {
          return new Date(s1.date).getTime() - new Date(s2.date).getTime();
        });
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
          "X-CSRFToken": `${userStore().token}`,
        },
        credentials: "include",
      });
    };

    /**
     * Supprime le schedule d'uuid uuid
     * @param uuid l'uuid du schedule a supprimer
     */
    const deleteSchedule = async (uuid: string | undefined) => {
      const token = userStore().token;
      const response = await useAPI(`/schedules/delete/${uuid}/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": `${token}`,
        },
        credentials: "include",
      });
      if (schedules.value)
        schedules.value = schedules.value.filter((s) => s.uuid !== uuid);
      closeModal();
    };

    onMounted(() => {
      fetchSchedules();
    });

    return {
      sessions,
      schedules,
      sortedSchedules,
      changeCanSubscribe,
      openModal,
      closeModal,
      deleteSchedule,
      selectedScheduleUuid,
      isModalOpen,
    };
  },
};
</script>

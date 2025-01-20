<template>
  <div
    id="popup-modal"
    tabindex="-1"
    v-show="showModal"
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
            @click="processDelete(selectedSessionSlug)"
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
  <Navbar />
  <div class="container mx-auto p-6">
    <h2 class="text-3xl font-semibold text-gray-800 mb-6">Sessions</h2>

    <ul class="space-y-4">
      <li
        v-for="session in asessions"
        :key="session.slug"
        class="flex justify-between items-center p-4 bg-white border border-gray-200 rounded-lg shadow-lg hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 transition-all"
      >
        <NuxtLink
          :to="`/sessions/${session.slug}`"
          class="text-lg font-semibold text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-500"
        >
          {{ session.name }}
        </NuxtLink>
        <button
          @click="openModal(session.slug)"
          v-if="userStore().isAdmin()"
          class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
        >
          Supprimer
        </button>
        <NuxtLink
          v-if="userStore().isTeacher()"
          :to="`/sessions/add-courses/${session.slug}/`"
          class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
        >
          Ajouter des cours
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import Navbar from "~/components/ui/navbar/Navbar.vue";

const showModal = ref<boolean>(false);
const selectedSessionSlug = ref<string | null>(null);
const modalTitle = ref<string>("");
const modalMessage = ref<string>("");

const { data: asessions } = await useAPI<ISessions>("/sessions/");

const openModal = (slug: string) => {
  selectedSessionSlug.value = slug;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedSessionSlug.value = null;
};

const processDelete = async (slug: string | null) => {
  try {
    await useAPI(`/sessions/${slug}/delete/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": `${userStore().token}`,
      },
      credentials: "include",
    });
    if (asessions.value) {
      asessions.value = asessions.value.filter(
        (session) => session.slug !== slug
      );
    }
    closeModal();
  } catch (error) {
    console.error("Error deleting session:", error);
  }
};
</script>

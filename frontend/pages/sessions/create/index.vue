<template>
  <Navbar />
  <div class="container mx-auto p-6">
    <form
      @submit.prevent="save"
      class="bg-white p-8 rounded-lg shadow-lg max-w-lg mx-auto"
    >
      <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">
        Créer une session
      </h2>

      <div class="mb-6">
        <label
          for="name"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Nom de la session</label
        >
        <input
          type="text"
          v-model="name"
          name="name"
          class="mt-2 w-full p-3 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500"
          required
        />
      </div>

      <button
        type="submit"
        class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700"
      >
        Valider
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";
import Navbar from "~/components/ui/navbar/Navbar.vue";

export default {
  components: {
    Navbar,
  },
  setup() {
    const name = ref<string>("");

    const save = async () => {
      if (!name.value) {
        alert("Le nom de la session est requis");
        return;
      }

      const data = {
        name: name.value,
      };

      try {
        const response = await useAPI(`/sessions/create/`, {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": `${userStore().token}`,
          },
          credentials: "include",
        });
        if (response.status.value === "success") {
          return navigateTo(`/`);
        }
      } catch (error) {}
    };

    return { name, save };
  },
};
</script>

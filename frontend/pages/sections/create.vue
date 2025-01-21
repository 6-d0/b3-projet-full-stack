<template>
  <Navbar />
  <div class="container mx-auto p-6">
    <form
      @submit.prevent="save"
      class="bg-white p-8 rounded-lg shadow-lg max-w-lg mx-auto"
    >
      <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">
        Créer une Branche
      </h2>

      <!-- Nom de la Branche -->
      <div class="mb-6">
        <label
          for="name"
          class="block text-sm font-medium text-gray-700"
        >
          Nom de la Branche
        </label>
        <input
          type="text"
          v-model="name"
          name="name"
          placeholder="Entrez le nom de la branche"
          class="mt-2 w-full p-3 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          required
        />
      </div>

      <button
        type="submit"
        class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300"
      >
        Sauvegarder
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";
import { useAPI } from "~/composables/useAPI";
import Navbar from "~/components/ui/navbar/Navbar.vue";

// Définir un type pour la réponse de l'API
interface Branch {
  slug: string;
  uuid: string;
  name: string;
  pk: number;
  courses: Course[];
}

interface Course {
  uuid: string;
  id: number;
  name: string;
  slug: string;
  teacher_name: string;
  teacher: {
    uuid: string;
    username: string;
    pk: number;
    last_name: string;
    first_name: string;
    role: string;
    email: string;
  };
}

export default {
  components: {
    Navbar,
  },
  setup() {
    const name = ref<string>("");

    const save = async () => {
      if (!name.value) {
        alert("Le nom de la Branche est requis");
        return;
      }

      const data = {
        name: name.value,
      };

      try {
        const { data: responseData, error } = await useAPI<Branch[]>(
          `/branches/create/`,
          {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": `${userStore().token}`, // Assurez-vous que cela récupère bien le token
            },
            credentials: "include",
          }
        );

        if (error.value) {
          console.error("Erreur dans la requête :", error.value);
          alert("Une erreur est survenue lors de la création de la branche.");
          return;
        }

        if (responseData.value) {
          alert("Branche créée avec succès !");
          navigateTo(`/`);
        } else {
          alert("Une erreur inattendue s'est produite.");
        }
      } catch (error) {
        console.error("Erreur lors de la création de la branche :", error);
        alert("Une erreur est survenue lors de la création de la branche.");
      }
    };

    return { name, save };
  },
};
</script>

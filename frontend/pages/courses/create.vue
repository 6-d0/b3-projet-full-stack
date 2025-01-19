<template>
  <Navbar />
  <div class="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-lg">
    <form @submit.prevent="save" class="space-y-6">
      <div class="space-y-2">
        <label for="name" class="block text-lg font-semibold text-gray-700"
          >Nom du cours</label
        >
        <input
          type="text"
          name="name"
          id="name"
          v-model="name"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Entrez le nom du cours"
        />
      </div>

      <div class="space-y-2">
        <label for="session" class="block text-lg font-semibold text-gray-700"
          >Session</label
        >
        <select
          name="session"
          id="session"
          v-model="selectedSession"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option
            v-for="session in sessions"
            :key="session.slug"
            :value="session.slug"
          >
            {{ session.name }}
          </option>
        </select>
      </div>

      <div class="space-y-2">
        <label for="branch" class="block text-lg font-semibold text-gray-700"
          >Branche</label
        >
        <select
          name="branch"
          id="branch"
          v-model="selectedBranch"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option
            v-for="branch in branchs"
            :key="branch.slug"
            :value="branch.slug"
          >
            {{ branch.name }}
          </option>
        </select>
      </div>

      <div>
        <input
          type="submit"
          value="Créer le cours"
          class="w-full py-3 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import Navbar from "~/components/ui/navbar/Navbar.vue";
export default {
  setup() {
    const sessions = ref<ISession[] | null>(null);
    const branchs = ref<IBranch[] | null>(null);
    const selectedSession = ref<string | null>(null);
    const selectedBranch = ref<string | null>(null);
    const name = ref<String>("");

    const fetchSession = async () => {
      const { data: asessions } = await useAPI<ISessions>(`/sessions/`);
      console.log(asessions.value);
      if (asessions.value) {
        sessions.value = asessions.value;
        selectedSession.value = sessions.value[0]?.slug || null;
      }
    };

    const fetchBranches = async (slug: string | null) => {
      const { data: abranchs } = await useAPI<IBranch[]>(`/branches/${slug}/`);
      console.log(abranchs.value);
      if (abranchs.value) {
        branchs.value = abranchs.value;
      }
    };

    watch(selectedSession, (newSlug) => {
      if (newSlug) {
        fetchBranches(newSlug);
      }
    });

    onMounted(() => {
      fetchSession();
    });

    const save = async () => {
      const data = {
        name: name.value,
        session: selectedSession.value || "",
        branch: selectedBranch.value || "",
      };
      const response = await useAPI(`/courses/create/`, {
        method: "POST",
        body: data,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": `${userStore().token}`,
        },
      });
    };

    return {
      sessions,
      branchs,
      name,
      save,
      selectedSession,
      selectedBranch,
    };
  },
};
</script>

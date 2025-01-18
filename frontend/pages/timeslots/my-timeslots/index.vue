<template>
  <Navbar />
  <div v-for="registration in registrations">
    {{ registration }}
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

const route = useRoute();
import { userStore } from "~/stores/user";
import authGlobal from "~/middleware/auth.global";
import Navbar from "~/components/ui/navbar/Navbar.vue";

export default {
  setup() {
    definePageMeta({
      middleware: authGlobal,
      roles: ["student"],
    });
    const user = userStore().user;
    const registrations = ref<IRegistration[] | null>(null);
    const fetchRegistrations = async () => {
      const { data: aregistrations } = await useAPI<IRegistration[] | null>(
        "/registrations/my-registrations"
      );
      if (aregistrations.value) registrations.value = aregistrations.value;
    };

    onMounted(async () => {
      fetchRegistrations();
    });

    return {
      user,
      registrations,
    };
  },
};
</script>

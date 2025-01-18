<template>
  <Navbar />
  <div>
    <div v-if="registration">
      <h1 class="text-2xl font-bold">
        Nom du cours : {{ registration.course.name }}
      </h1>
      <div class="">
        Professeur: {{ registration.course.teacher.last_name.toUpperCase() }}
        {{ registration.course.teacher.first_name }}
      </div>
      <div class="" v-if="registration.comment">
        Commentaire : {{ registration.comment }}
      </div>
      <div class="">
        Date d'inscription:
        {{ registration.date.toLocaleDateString() }}
      </div>
      <div class="">
        Date de visite:
        {{ registration.slot.schedule.date.toLocaleDateString() }}
      </div>
    </div>
    <p v-else>Chargement...</p>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

import { userStore } from "~/stores/user";
import Navbar from "~/components/ui/navbar/Navbar.vue";

export default defineComponent({
  name: "RegistrationDetails",
  components: { Navbar },
  setup() {
    const route = useRoute();
    const registration = ref<IRegistration>();

    const fetchRegistration = async () => {
      const { data: aregistrations } = await useAPI<IRegistration[] | null>(
        "/registrations/my-registrations"
      );
      if (aregistrations && aregistrations.value) {
        registration.value = aregistrations.value.find(
          (r) => r.uuid === route.params.registration_uuid
        ) as IRegistration;
        registration.value.date = new Date(registration.value.date);
        registration.value.slot.schedule.date = new Date(
          registration.value.slot.schedule.date
        );
      }
    };

    fetchRegistration();
    return { registration };
  },
});
</script>

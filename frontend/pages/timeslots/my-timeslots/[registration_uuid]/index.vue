<template>
  <Navbar />
  <div class="container mx-auto px-4 py-8">
    <div v-if="registration" class="bg-white shadow rounded-lg p-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-4">
        {{ registration.course.name }}
      </h1>
      <div class="border-t border-gray-200 mt-4 pt-4">
        <h2 class="text-xl font-semibold text-gray-700">
          Détails du professeur
        </h2>
        <p class="mt-2">
          <span class="font-medium text-gray-600">Professeur :</span>
          {{ registration.course.teacher.last_name.toUpperCase() }}
          {{ registration.course.teacher.first_name }}
        </p>
        <p class="mt-1">
          <span class="font-medium text-gray-600">Mail : </span>
          <a
            :href="`mailto:${registration.course.teacher.email}`"
            class="text-blue-500 hover:underline"
          >
            {{ registration.course.teacher.email }}
          </a>
        </p>
        <p class="mt-1">
          <span class="font-medium text-gray-600">
            Nom d'utilisateur: {{ registration.course.teacher.username }}
          </span>
        </p>
      </div>

      <div
        v-if="registration.comment"
        class="border-t border-gray-200 mt-4 pt-4"
      >
        <h2 class="text-xl font-semibold text-gray-700">Commentaire</h2>
        <p class="mt-2 text-gray-600">{{ registration.comment }}</p>
      </div>

      <div class="border-t border-gray-200 mt-4 pt-4">
        <h2 class="text-xl font-semibold text-gray-700">Dates importantes</h2>
        <p class="mt-2">
          <span class="font-medium text-gray-600">Date d'inscription :</span>
          {{ registration.date.toLocaleDateString() }}
        </p>
        <p class="mt-1">
          <span class="font-medium text-gray-600">Date de visite :</span>
          {{ registration.slot.schedule.date.toLocaleDateString() }}
        </p>
      </div>

      <div class="border-t border-gray-200 mt-4 pt-4">
        <h2 class="text-xl font-semibold text-gray-700">Heure de passage</h2>
        <p class="mt-2">
          <span class="font-medium text-gray-600">De :</span>
          {{ formatTime(new Date(registration.slot.begin_time)) }}
        </p>
        <p class="mt-1">
          <span class="font-medium text-gray-600">À : </span>
          {{ formatTime(new Date(registration.slot.end_time)) }}
        </p>
      </div>
    </div>
    <p v-else class="text-center text-gray-500">Chargement...</p>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

import { userStore } from "~/stores/user";
import Navbar from "~/components/ui/navbar/Navbar.vue";
import { NuxtLink } from "#build/components";

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

    function formatTime(d: Date) {
      let hours = d.getHours();
      let minutes = d.getMinutes();
      const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
      return `${lzero(hours)}:${lzero(minutes)}`;
    }

    fetchRegistration();
    return { registration, formatTime };
  },
});
</script>

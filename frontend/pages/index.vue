<template>
  <Navbar />
  <div class="container mx-auto p-6">
    <h2 class="text-3xl font-semibold text-gray-800 mb-6">Sessions</h2>

    <ul class="space-y-4">
      <li
        v-for="session in asessions"
        :key="session.slug"
        class="p-4 bg-white border border-gray-200 rounded-lg shadow-lg hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 transition-all"
      >
        <NuxtLink
          :to="`/sessions/${session.slug}`"
          class="text-lg font-semibold text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-500"
        >
          {{ session.name }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import Navbar from "~/components/ui/navbar/Navbar.vue";

const { data: asessions } = await useAPI<ISessions>("/sessions/");
</script>

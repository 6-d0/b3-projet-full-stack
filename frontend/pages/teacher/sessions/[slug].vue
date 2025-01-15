<template>
  <div class="container mx-auto p-6">
    <h3 class="text-2xl font-semibold text-gray-900 mb-6">
      <span>{{ session?.name }}</span>
    </h3>

    <ul class="space-y-4">
      <li
        v-for="branch in branches"
        :key="branch.slug"
        class="p-4 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 transition-all"
      >
        <NuxtLink
          :href="`/sessions/${route.params.slug}/${branch.slug}/`"
          class="text-lg font-medium text-gray-800 hover:text-blue-600 dark:text-gray-200 dark:hover:text-blue-400"
        >
          {{ branch.name }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
const route = useRoute();
const session_slug = route.params.slug;

const { data: asessions } = await useAPI<ISession[]>("/sessions/");
const session = asessions.value?.find((s) => s.slug === session_slug);

const { data: branches } = await useAPI<IBranch[]>(
  `/branches/${route.params.slug}`
);
</script>

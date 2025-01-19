<template>
  <div
    v-if="visible"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div
      class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg max-w-sm w-full"
    >
      <div class="mb-4">
        <h3 class="text-lg font-bold text-gray-800 dark:text-white">
          {{ title }}
        </h3>
      </div>
      <div class="mb-4 text-gray-700 dark:text-gray-300">
        <slot />
      </div>
      <div class="flex justify-end space-x-2">
        <button
          @click="onClose"
          class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
        >
          Fermer
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      default: "Message",
    },
  },
  emits: ["close"],
  methods: {
    onClose() {
      this.$emit("close");
    },
  },
};
</script>

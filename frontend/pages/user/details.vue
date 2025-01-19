<template>
  <Navbar />
  <div class="flex justify-center items-center bg-gradient-to-r">
    <div class="p-6 bg-white rounded-lg shadow-lg max-w-md w-full space-y-4">
      <div class="space-y-1">
        <div class="text-lg font-semibold text-indigo-800">First Name</div>
        <div class="text-xl text-gray-900">{{ user?.first_name }}</div>
      </div>

      <div class="space-y-1">
        <div class="text-lg font-semibold text-indigo-800">Last Name</div>
        <div class="text-xl text-gray-900">{{ user?.last_name }}</div>
      </div>

      <div class="space-y-1">
        <div class="text-lg font-semibold text-indigo-800">Username</div>
        <div class="text-xl text-gray-900">{{ user?.username }}</div>
      </div>

      <div class="space-y-1">
        <div class="text-lg font-semibold text-indigo-800">Email</div>
        <a :href="`mailto:${user?.email}`" class="text-xl text-blue-600">{{
          user?.email
        }}</a>
      </div>

      <div class="space-y-1">
        <div class="text-lg font-semibold text-indigo-800">Role</div>
        <div class="text-xl text-gray-900">
          {{
            user?.role
              ? user?.role.charAt(0).toUpperCase() +
                user?.role.slice(1).toLowerCase()
              : ""
          }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { userStore } from "@/stores/user";

export default defineComponent({
  setup() {
    const store = userStore();
    const user = store.user;

    return { user };
  },
});
</script>

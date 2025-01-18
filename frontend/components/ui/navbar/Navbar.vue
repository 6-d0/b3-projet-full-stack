<script lang="ts">
import { NuxtLink } from "#build/components";
import { defineComponent } from "vue";
export default defineComponent({
  name: "Navbar",
  computed: {
    isStudent() {
      const user = userStore().user;
      return user?.role === "student";
    },
    isTeacher() {
      const user = userStore().user;
      return user?.role === "teacher";
    },
  },
});
</script>

<template>
  <header
    class="lg:px-16 px-4 bg-white flex flex-wrap items-center py-4 shadow-md mb-4 static w-full"
  >
    <div class="flex-1 flex justify-between items-center">
      <a href="#" class="text-xl">reviewcopies</a>
    </div>
    <div class="hidden md:flex md:items-center md:w-auto w-full" id="menu">
      <nav>
        <ul
          class="md:flex items-center justify-between text-base text-gray-700 pt-4 md:pt-0"
        >
          <li class="md:p-4 py-3 px-0 block">
            <router-link to="/">Accueil</router-link>
          </li>
          <li v-if="isStudent" class="md:p-4 py-3 px-0 block">
            <router-link to="/timeslots/my-timeslots"
              >Mes inscriptions</router-link
            >
          </li>
          <li class="md:p-4 py-3 px-0 block">
            <router-link to="#">Services</router-link>
          </li>
          <li class="md:p-4 py-3 px-0 block">
            <router-link to="#">Contact</router-link>
          </li>
          <li class="md:p-4 py-3 px-0 block">
            <NuxtLink :to="`#`">Se déconnecter</NuxtLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

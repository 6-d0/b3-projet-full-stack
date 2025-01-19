<script lang="ts">
import { NuxtLink } from "#build/components";
import { defineComponent } from "vue";
import { userStore } from "@/stores/user";

export default defineComponent({
  name: "Navbar",
  computed: {
    user() {
      return userStore().user;
    },
    isStudent() {
      return this.user?.role === "student";
    },
    isTeacher() {
      return this.user?.role === "teacher";
    },
    isAdmin() {
      return this.user?.role === "admin";
    },
  },
  methods: {
    async logout() {
      try {
        const response = await fetch(`/api/v1/auth/logout/`, {
          body: null,
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        userStore().$reset();
      } catch (error) {
        console.error("Erreur lors de la déconnexion:", error);
      }
    },
  },
});
</script>

<template>
  <header
    class="lg:px-16 px-4 bg-white flex flex-wrap items-center py-4 shadow-md mb-4 static w-full"
  >
    <div class="flex-1 flex justify-between items-center">
      <a href="/" class="text-xl">reviewcopies</a>
    </div>
    <div class="hidden md:flex md:items-center md:w-auto w-full" id="menu">
      <nav>
        <ul
          class="md:flex items-center justify-between text-base text-gray-700 pt-4 md:pt-0"
        >
          <NuxtLink to="/">
            <li class="md:p-4 py-3 px-0 block hover:bg-gray-50">Accueil</li>
          </NuxtLink>
          <li v-if="isStudent" class="md:p-4 py-3 px-0 block hover:bg-gray-50">
            <NuxtLink to="/timeslots/my-timeslots"> Mes inscriptions </NuxtLink>
          </li>
          <NuxtLink to="/schedules/">
            <li
              class="md:p-4 py-3 px-0 block hover:bg-gray-50"
              v-if="user?.role === 'teacher'"
            >
              Créer un planning
            </li>
          </NuxtLink>
          <NuxtLink to="/schedules/my-schedules">
            <li
              class="md:p-4 py-3 px-0 block hover:bg-gray-50"
              v-if="isTeacher"
            >
              Mes plannings
            </li>
          </NuxtLink>

          <li
            class="md:p-6 py-4 cursor-pointer px-0 block relative group hover:bg-gray-50"
            v-if="isTeacher"
          >
            <span class="">Cours</span>
            <ul
              class="absolute hidden group-hover:block bg-white shadow-lg rounded-lg mt-4 w-56 text-base -left-4"
            >
              <NuxtLink to="/courses/create/">
                <li class="px-6 py-3 hover:bg-gray-50 text-lg">
                  Créer un cours
                </li>
              </NuxtLink>
              <NuxtLink to="/courses/details/">
                <li class="px-6 py-3 hover:bg-gray-50 text-lg">Mes cours</li>
              </NuxtLink>
            </ul>
          </li>
          <li class="md:p-4 py-3 px-0 block" v-if="isAdmin">
            <NuxtLink to="/sessions/create/"> Créer une session </NuxtLink>
          </li>
          <li
            class="md:p-6 py-4 px-0 block relative group cursor-pointer hover:bg-gray-50"
          >
            <span
              class="cursor-pointer hover:text-gray-500 text-lg font-semibold"
              v-if="user?.last_name && user.first_name"
            >
              {{ user?.last_name.toUpperCase() }} {{ user?.first_name }}
            </span>
            <span
              v-else
              class="cursor-pointer hover:text-gray-500 text-lg font-semibold"
            >
              Administrateur
            </span>
            <ul
              class="absolute hidden group-hover:block bg-white shadow-lg rounded-lg mt-4 w-56 text-base -left-4"
            >
              <NuxtLink class="py-3 w-[100%]" :to="`/user/details`">
                <li class="px-6 py-3 hover:bg-gray-50 text-lg">Mon profil</li>
              </NuxtLink>
              <li class="px-6 py-3 hover:bg-gray-50 text-lg" @click="logout">
                Se déconnecter
              </li>
            </ul>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

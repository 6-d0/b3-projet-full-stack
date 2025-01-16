import { defineStore } from "pinia";

export const userStore = defineStore("user", {
  state: () => ({
    user: null as IUser | null, // Utilisateur actuel (ou null si non connecté)
    token: null as string | null,
  }),
  actions: {
    async fetchUser() {
      if (this.user) return;

      const { data, error } = await useAPI("/user/details/", {
        credentials: "include",
      });

      if (!error.value) {
        this.user = data.value as IUser;
      } else {
        console.error("Failed to load user:", error.value);
        throw createError({
          statusCode: 444,
          statusMessage: "Failed to load user",
        });
      }
    },
  },
});

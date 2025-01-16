export default defineNuxtRouteMiddleware(async (to, from) => {
  const store = userStore();

  if (!store.user) {
    const { data, error } = await useAPI("/user/details/", {
      credentials: "include",
    });
    if (!error.value) {
      store.token = document.cookie.split("=")[1];
      store.user = data.value as IUser;
    } else if (error?.value?.statusCode == 403) {
      return await navigateTo(`/auth/login/?next=${to.path}`, {
        external: true,
      });
    } else {
      console.log(error);
      throw createError({ statusCode: 444, statusMessage: "Failed to login" });
    }
  }
  const requiredRoles = (to.meta.roles as string[]) || [];
  const userRole = store.user.role;

  if (requiredRoles.length != 0 && !requiredRoles.includes(userRole)) {
    return await navigateTo("/unauthorized/");
  } else {
    console.log(`c'est ok ${store.user.role}`);
  }
});

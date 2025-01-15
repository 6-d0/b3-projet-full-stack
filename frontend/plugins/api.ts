export default defineNuxtPlugin((nuxtApp) => {
  const api = $fetch.create({
    baseURL: '/api/v1',
    async onResponseError({ response }) {
      if (response.status === 403) {
          await nuxtApp.runWithContext(() => navigateTo('/auth/login/', { external: true }))
      }
    }
  })

  return {
    provide: {
      api
    }
  }
})

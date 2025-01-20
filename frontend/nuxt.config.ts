// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-04-03',
    devtools: { enabled: true },
    typescript: {
        typeCheck: true,
    },
    ssr: false,
    modules: ['@nuxtjs/tailwindcss', '@nuxtjs/color-mode', '@pinia/nuxt', 'shadcn-nuxt'],
    shadcn: {
        prefix: '',
        componentDir: './components/ui'
    },
})

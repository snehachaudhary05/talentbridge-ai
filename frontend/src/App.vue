<template>
  <div id="app" class="min-h-screen">
    <Navbar v-if="!isAuthPage" />
    <main :class="{ 'pt-16': !isAuthPage }">
      <router-view />
    </main>
    <Footer v-if="!isAuthPage" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

const route = useRoute()

const isAuthPage = computed(() => {
  return ['/login', '/register'].includes(route.path)
})
</script>

<style scoped>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

<template>
  <footer class="bg-gray-900 text-gray-300 mt-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Company Info -->
        <div class="col-span-1">
          <div class="flex items-center space-x-2 mb-4">
            <div class="bg-primary-600 p-2 rounded-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <span class="text-xl font-bold text-white">JobPortal<span class="text-primary-400">AI</span></span>
          </div>
          <p class="text-sm text-gray-400">
            AI-powered job portal helping candidates find their dream jobs and recruiters find top talent.
          </p>
        </div>

        <!-- For Candidates -->
        <div>
          <h3 class="text-white font-semibold mb-4">For Candidates</h3>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/jobs" class="hover:text-primary-400 transition">Browse Jobs</router-link></li>
            <li><router-link to="/ai-assistant" class="hover:text-primary-400 transition">AI Resume Analysis</router-link></li>
            <li><router-link to="/ai-assistant" class="hover:text-primary-400 transition">Job Matching</router-link></li>
            <li><router-link to="/register" class="hover:text-primary-400 transition">Create Account</router-link></li>
          </ul>
        </div>

        <!-- For Recruiters -->
        <div>
          <h3 class="text-white font-semibold mb-4">For Recruiters</h3>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/post-job" class="hover:text-primary-400 transition">Post a Job</router-link></li>
            <li><router-link to="/dashboard" class="hover:text-primary-400 transition">Dashboard</router-link></li>
            <li><router-link to="/ai-assistant" class="hover:text-primary-400 transition">AI Candidate Screening</router-link></li>
            <li><router-link to="/interviews" class="hover:text-primary-400 transition">Manage Interviews</router-link></li>
          </ul>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-white font-semibold mb-4">Quick Links</h3>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/" class="hover:text-primary-400 transition">Home</router-link></li>
            <li><router-link to="/saved-jobs" class="hover:text-primary-400 transition">Saved Jobs</router-link></li>
            <li><router-link to="/interviews" class="hover:text-primary-400 transition">My Interviews</router-link></li>
            <li><router-link to="/profile" class="hover:text-primary-400 transition">Profile Settings</router-link></li>
          </ul>
        </div>
      </div>

      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
        <p>&copy; 2026 JobPortalAI. All rights reserved. Powered by FREE Mock AI.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

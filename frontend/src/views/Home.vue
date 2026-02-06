<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Find Your Dream Job with <span class="text-primary-200">AI</span>
            </h1>
            <p class="text-xl text-primary-100 mb-8">
              AI-powered job matching, resume analysis, and career guidance. Get personalized recommendations instantly.
            </p>
            <div class="flex space-x-4">
              <router-link to="/register" class="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition shadow-lg">
                Get Started Free
              </router-link>
              <router-link to="/jobs" class="bg-primary-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-400 transition">
                Browse Jobs
              </router-link>
            </div>
            <div class="mt-8 flex items-center space-x-6 text-sm text-primary-100">
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                100% Free
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                No API Key Needed
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                AI-Powered
              </div>
            </div>
          </div>
          <div class="hidden md:block">
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
              <div class="space-y-4">
                <div class="bg-white rounded-lg p-4 shadow-lg">
                  <div class="flex items-start space-x-3">
                    <div class="bg-green-100 p-2 rounded-lg">
                      <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                    <div class="flex-1">
                      <div class="flex items-center justify-between">
                        <span class="text-gray-900 font-semibold">Match Score: 94%</span>
                        <span class="badge badge-success">High Match</span>
                      </div>
                      <p class="text-sm text-gray-600 mt-1">Senior Python Developer</p>
                    </div>
                  </div>
                </div>
                <div class="bg-white rounded-lg p-4 shadow-lg">
                  <div class="flex items-start space-x-3">
                    <div class="bg-blue-100 p-2 rounded-lg">
                      <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                      </svg>
                    </div>
                    <div class="flex-1">
                      <span class="text-gray-900 font-semibold">AI Analysis Complete</span>
                      <p class="text-sm text-gray-600 mt-1">Resume score: 87/100</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">Powered by AI</h2>
          <p class="text-xl text-gray-600">Everything you need to find your perfect job</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="card text-center">
            <div class="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Resume Analysis</h3>
            <p class="text-gray-600">Get instant AI-powered feedback on your resume. Improve your ATS score and stand out.</p>
          </div>

          <!-- Feature 2 -->
          <div class="card text-center">
            <div class="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Smart Job Matching</h3>
            <p class="text-gray-600">AI matches your skills with perfect job opportunities. Get personalized recommendations.</p>
          </div>

          <!-- Feature 3 -->
          <div class="card text-center">
            <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Skill Recommendations</h3>
            <p class="text-gray-600">Discover which skills to learn next. Get a personalized roadmap for your career growth.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-4 gap-8 text-center">
          <div>
            <div class="text-4xl font-bold text-primary-600 mb-2">1,250+</div>
            <div class="text-gray-600">Active Users</div>
          </div>
          <div>
            <div class="text-4xl font-bold text-primary-600 mb-2">450+</div>
            <div class="text-gray-600">Job Listings</div>
          </div>
          <div>
            <div class="text-4xl font-bold text-primary-600 mb-2">3,200+</div>
            <div class="text-gray-600">Applications</div>
          </div>
          <div>
            <div class="text-4xl font-bold text-primary-600 mb-2">94%</div>
            <div class="text-gray-600">Success Rate</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-primary-600 text-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl font-bold mb-4">Ready to Find Your Dream Job?</h2>
        <p class="text-xl text-primary-100 mb-8">Join thousands of candidates using AI to accelerate their career</p>
        <router-link to="/register" class="inline-block bg-white text-primary-600 px-10 py-4 rounded-lg font-semibold hover:bg-primary-50 transition shadow-lg text-lg">
          Get Started for Free
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

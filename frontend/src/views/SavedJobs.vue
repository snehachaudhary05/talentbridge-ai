<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Saved Jobs</h1>
      <p class="text-xl text-gray-600">Jobs you've bookmarked for later</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600">Loading saved jobs...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="savedJobs.length === 0" class="text-center py-12">
      <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">No saved jobs yet</h3>
      <p class="text-gray-600 mb-4">Start browsing jobs and save the ones you're interested in</p>
      <router-link to="/jobs" class="btn-primary inline-block">Browse Jobs</router-link>
    </div>

    <!-- Saved Jobs List -->
    <div v-else>
      <div class="mb-4 text-gray-600">
        {{ savedJobs.length }} {{ savedJobs.length === 1 ? 'saved job' : 'saved jobs' }}
      </div>

      <div class="grid gap-6">
        <div
          v-for="savedJob in savedJobs"
          :key="savedJob.id"
          class="card hover:border-primary-300 cursor-pointer transition-all"
          @click="viewJob(savedJob.job_details.id)"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-start justify-between mb-2">
                <h3 class="text-xl font-bold text-gray-900">{{ savedJob.job_details.title }}</h3>
                <button
                  @click.stop="unsaveJob(savedJob)"
                  class="ml-3 p-2 rounded-full hover:bg-gray-100 transition-colors flex-shrink-0"
                  title="Remove from saved jobs"
                >
                  <svg
                    class="w-6 h-6 text-yellow-500 fill-yellow-500 transition-colors"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                    ></path>
                  </svg>
                </button>
              </div>
              <p class="text-lg text-gray-700 mb-3">{{ savedJob.job_details.company_name }}</p>
              <div class="flex flex-wrap gap-2 mb-3">
                <span class="badge badge-info">{{ formatJobType(savedJob.job_details.job_type) }}</span>
                <span v-if="savedJob.job_details.is_remote" class="badge badge-success">Remote</span>
                <span class="badge bg-purple-100 text-purple-800">
                  <svg class="w-3 h-3 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                  </svg>
                  Saved {{ formatDate(savedJob.created_at) }}
                </span>
              </div>
              <div class="flex items-center text-sm text-gray-600 space-x-4 mb-3">
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  {{ savedJob.job_details.location }}
                </span>
                <span v-if="savedJob.job_details.salary_min" class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  ${{ savedJob.job_details.salary_min.toLocaleString() }} - ${{ savedJob.job_details.salary_max.toLocaleString() }}
                </span>
              </div>

              <!-- Personal Notes -->
              <div v-if="savedJob.notes" class="mt-3 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                <p class="text-sm text-gray-700">
                  <span class="font-semibold">Notes:</span> {{ savedJob.notes }}
                </p>
              </div>
            </div>
            <svg class="w-6 h-6 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const savedJobs = ref([])
const loading = ref(true)

const fetchSavedJobs = async () => {
  loading.value = true
  try {
    const response = await axios.get('/jobs/saved-jobs/')
    console.log('Saved jobs response:', response.data)
    savedJobs.value = response.data
  } catch (error) {
    console.error('Error fetching saved jobs:', error)
    alert('Failed to load saved jobs')
  } finally {
    loading.value = false
  }
}

const unsaveJob = async (savedJob) => {
  try {
    await axios.post('/jobs/saved-jobs/unsave_job/', { job_id: savedJob.job })
    // Remove from list
    savedJobs.value = savedJobs.value.filter(sj => sj.id !== savedJob.id)
  } catch (error) {
    console.error('Error unsaving job:', error)
    alert('Failed to unsave job. Please try again.')
  }
}

const viewJob = (id) => {
  router.push(`/jobs/${id}`)
}

const formatJobType = (type) => {
  if (!type) return ''
  return type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return date.toLocaleDateString()
}

onMounted(() => {
  fetchSavedJobs()
})
</script>

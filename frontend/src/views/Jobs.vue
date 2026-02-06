<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">
        {{ authStore.isRecruiter ? 'My Job Posts' : 'Browse Jobs' }}
      </h1>
      <p class="text-xl text-gray-600">
        {{ authStore.isRecruiter ? 'Manage your job postings' : 'Discover your next opportunity' }}
      </p>
    </div>

    <!-- Enhanced Filters (Candidates Only) -->
    <div v-if="authStore.isCandidate" class="card mb-8">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Filter Jobs</h3>

      <div class="grid md:grid-cols-3 gap-4 mb-4">
        <!-- Skills Search -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Skills</label>
          <input
            v-model="filters.skills"
            type="text"
            placeholder="e.g., Python, React, Django"
            class="input-field"
          />
        </div>

        <!-- Location -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
          <input
            v-model="filters.location"
            type="text"
            placeholder="e.g., San Francisco"
            class="input-field"
            list="locations"
          />
          <datalist id="locations">
            <option v-for="loc in filterOptions.locations" :key="loc" :value="loc">{{ loc }}</option>
          </datalist>
        </div>

        <!-- Company -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Company</label>
          <input
            v-model="filters.company"
            type="text"
            placeholder="e.g., Google"
            class="input-field"
            list="companies"
          />
          <datalist id="companies">
            <option v-for="comp in filterOptions.companies" :key="comp" :value="comp">{{ comp }}</option>
          </datalist>
        </div>
      </div>

      <div class="grid md:grid-cols-3 gap-4 mb-4">
        <!-- Job Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Job Type</label>
          <select v-model="filters.job_type" class="input-field">
            <option value="">All Types</option>
            <option v-for="type in filterOptions.job_types" :key="type" :value="type">
              {{ formatJobType(type) }}
            </option>
          </select>
        </div>

        <!-- Salary Range -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Min Salary: ${{ filters.salary_min !== null ? filters.salary_min.toLocaleString() : 'Any' }}
          </label>
          <input
            v-model.number="filters.salary_min"
            type="range"
            :min="filterOptions.salary_range.min"
            :max="filterOptions.salary_range.max"
            :step="5000"
            class="w-full"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Max Salary: ${{ filters.salary_max !== null ? filters.salary_max.toLocaleString() : 'Any' }}
          </label>
          <input
            v-model.number="filters.salary_max"
            type="range"
            :min="filterOptions.salary_range.min"
            :max="filterOptions.salary_range.max"
            :step="5000"
            class="w-full"
          />
        </div>
      </div>

      <div class="grid md:grid-cols-2 gap-4 mb-4">
        <!-- Experience Range -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Min Experience: {{ filters.experience_min !== null ? filters.experience_min : 'Any' }} years
          </label>
          <input
            v-model.number="filters.experience_min"
            type="range"
            :min="filterOptions.experience_range.min"
            :max="filterOptions.experience_range.max"
            class="w-full"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Max Experience: {{ filters.experience_max !== null ? filters.experience_max : 'Any' }} years
          </label>
          <input
            v-model.number="filters.experience_max"
            type="range"
            :min="filterOptions.experience_range.min"
            :max="filterOptions.experience_range.max"
            class="w-full"
          />
        </div>
      </div>

      <div class="flex gap-3">
        <button @click="applyFilters" class="btn-primary">
          Apply Filters
        </button>
        <button @click="clearFilters" class="btn-secondary">
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Job Listings -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600">Loading jobs...</p>
    </div>

    <div v-else-if="jobs.length === 0" class="text-center py-12">
      <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">
        {{ authStore.isRecruiter ? 'No jobs posted yet' : 'No jobs found' }}
      </h3>
      <p class="text-gray-600">
        {{ authStore.isRecruiter ? 'Start by posting your first job' : 'Try adjusting your search criteria' }}
      </p>
      <router-link v-if="authStore.isRecruiter" to="/post-job" class="btn-primary mt-4 inline-block">
        Post Your First Job
      </router-link>
    </div>

    <div v-else>
      <div class="mb-4 text-gray-600">
        Found {{ jobs.length }} {{ jobs.length === 1 ? 'job' : 'jobs' }}
      </div>

      <div class="grid gap-6">
        <!-- Recruiter View: Job Management Cards -->
        <div v-if="authStore.isRecruiter" v-for="job in jobs" :key="job.id" class="card">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
            <div class="flex-1 min-w-0">
              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 mb-2">
                <h3 class="text-lg sm:text-xl font-bold text-gray-900 break-words">{{ job.title }}</h3>
                <span class="badge self-start" :class="job.status === 'published' ? 'badge-success' : 'badge-warning'">
                  {{ job.status }}
                </span>
              </div>
              <p class="text-base sm:text-lg text-gray-700 mb-3">{{ job.company_name }}</p>
              <div class="flex flex-wrap gap-2 mb-3">
                <span class="badge badge-info">{{ formatJobType(job.job_type) }}</span>
                <span v-if="job.is_remote" class="badge badge-success">Remote</span>
                <span class="badge badge-primary">
                  {{ job.applications_count || 0 }} Applications
                </span>
              </div>
              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-sm text-gray-600">
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  {{ job.location }}
                </span>
                <span v-if="job.salary_min" class="flex items-center">
                  <svg class="w-4 h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  ${{ job.salary_min.toLocaleString() }} - ${{ job.salary_max.toLocaleString() }}
                </span>
              </div>
            </div>
            <div class="flex flex-row sm:flex-col gap-2">
              <button @click="viewJob(job.id)" class="btn-primary text-sm flex-1 sm:flex-none">
                View Details
              </button>
              <button @click="toggleStatus(job)" class="btn-secondary text-sm flex-1 sm:flex-none">
                {{ job.status === 'published' ? 'Unpublish' : 'Publish' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Candidate View: Browse Jobs Cards -->
        <div v-else v-for="job in jobs" :key="job.id" class="card hover:border-primary-300 cursor-pointer transition-all" @click="viewJob(job.id)">
          <div class="flex justify-between items-start gap-3">
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2 mb-2">
                <h3 class="text-lg sm:text-xl font-bold text-gray-900 break-words flex-1">{{ job.title }}</h3>
                <button
                  @click.stop="toggleSaveJob(job)"
                  class="p-2 rounded-full hover:bg-gray-100 transition-colors flex-shrink-0"
                  :title="job.is_saved ? 'Remove from saved jobs' : 'Save job'"
                >
                  <svg
                    class="w-5 h-5 sm:w-6 sm:h-6 transition-colors"
                    :class="job.is_saved ? 'text-yellow-500 fill-yellow-500' : 'text-gray-400'"
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
              <p class="text-base sm:text-lg text-gray-700 mb-3">{{ job.company_name }}</p>
              <div class="flex flex-wrap gap-2 mb-3">
                <span class="badge badge-info">{{ formatJobType(job.job_type) }}</span>
                <span v-if="job.is_remote" class="badge badge-success">Remote</span>
                <span v-if="isJobApplied(job.id)" class="badge bg-blue-100 text-blue-800">✓ Applied</span>
              </div>
              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-sm text-gray-600">
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  {{ job.location }}
                </span>
                <span v-if="job.salary_min" class="flex items-center">
                  <svg class="w-4 h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  ${{ job.salary_min.toLocaleString() }} - ${{ job.salary_max.toLocaleString() }}
                </span>
              </div>
            </div>
            <svg class="w-5 h-5 sm:w-6 sm:h-6 text-gray-400 flex-shrink-0 hidden sm:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

const jobs = ref([])
const loading = ref(true)
const appliedJobIds = ref(new Set())
const filters = ref({
  skills: '',
  location: '',
  company: '',
  job_type: '',
  salary_min: null,
  salary_max: null,
  experience_min: null,
  experience_max: null
})

const filterOptions = ref({
  companies: [],
  locations: [],
  job_types: [],
  salary_range: { min: 0, max: 200000 },
  experience_range: { min: 0, max: 20 }
})

// Track if filters have been applied by user
const filtersApplied = ref(false)

const fetchFilterOptions = async () => {
  try {
    const response = await axios.get('/api/jobs/jobs/filter_options/')
    filterOptions.value = response.data

    // Don't initialize slider values - let them stay null until user interacts
    // This ensures we don't send default filter values to backend
  } catch (error) {
    console.error('Error fetching filter options:', error)
  }
}

const fetchJobs = async () => {
  loading.value = true
  try {
    const params = {}

    // Only apply filters for candidates if they've explicitly applied filters
    if (authStore.isCandidate && filtersApplied.value) {
      // Text filters - only send if not empty
      if (filters.value.skills && filters.value.skills.trim()) {
        params.skills = filters.value.skills
      }
      if (filters.value.location && filters.value.location.trim()) {
        params.location = filters.value.location
      }
      if (filters.value.company && filters.value.company.trim()) {
        params.company = filters.value.company
      }
      if (filters.value.job_type) {
        params.job_type = filters.value.job_type
      }

      // Salary filters - only send if not null/undefined and not at default min/max
      if (filters.value.salary_min !== null &&
          filters.value.salary_min !== undefined &&
          filters.value.salary_min > filterOptions.value.salary_range.min) {
        params.salary_min = filters.value.salary_min
      }
      if (filters.value.salary_max !== null &&
          filters.value.salary_max !== undefined &&
          filters.value.salary_max < filterOptions.value.salary_range.max) {
        params.salary_max = filters.value.salary_max
      }

      // Experience filters - only send if not null/undefined and not at default min/max
      if (filters.value.experience_min !== null &&
          filters.value.experience_min !== undefined &&
          filters.value.experience_min > filterOptions.value.experience_range.min) {
        params.experience_min = filters.value.experience_min
      }
      if (filters.value.experience_max !== null &&
          filters.value.experience_max !== undefined &&
          filters.value.experience_max < filterOptions.value.experience_range.max) {
        params.experience_max = filters.value.experience_max
      }
    }

    const response = await axios.get('/api/jobs/jobs/', { params })
    jobs.value = response.data
  } catch (error) {
    console.error('Error fetching jobs:', error)
  } finally {
    loading.value = false
  }
}

const toggleStatus = async (job) => {
  try {
    const newStatus = job.status === 'published' ? 'draft' : 'published'
    await axios.patch(`/api/jobs/jobs/${job.id}/`, { status: newStatus })
    job.status = newStatus
    alert(`Job ${newStatus === 'published' ? 'published' : 'unpublished'} successfully!`)
  } catch (error) {
    alert('Error updating job status: ' + error.message)
  }
}

const applyFilters = () => {
  filtersApplied.value = true
  fetchJobs()
}

const clearFilters = () => {
  filtersApplied.value = false
  filters.value = {
    skills: '',
    location: '',
    company: '',
    job_type: '',
    salary_min: null,
    salary_max: null,
    experience_min: null,
    experience_max: null
  }
  fetchJobs()
}

const viewJob = (id) => {
  router.push(`/jobs/${id}`)
}

const formatJobType = (type) => {
  if (!type) return ''
  return type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const fetchAppliedJobs = async () => {
  if (authStore.isCandidate) {
    try {
      const response = await axios.get('/api/jobs/applications/')
      appliedJobIds.value = new Set(response.data.map(app => app.job))
    } catch (error) {
      console.error('Error fetching applied jobs:', error)
    }
  }
}

const isJobApplied = (jobId) => {
  return appliedJobIds.value.has(jobId)
}

const toggleSaveJob = async (job) => {
  try {
    if (job.is_saved) {
      // Unsave the job
      await axios.post('/api/jobs/saved-jobs/unsave_job/', { job_id: job.id })
      job.is_saved = false
    } else {
      // Save the job
      await axios.post('/api/jobs/saved-jobs/save_job/', { job_id: job.id })
      job.is_saved = true
    }
  } catch (error) {
    console.error('Error toggling saved job:', error)
    alert('Failed to save/unsave job. Please try again.')
  }
}

onMounted(async () => {
  await fetchFilterOptions()
  await fetchAppliedJobs()
  await fetchJobs()
})
</script>

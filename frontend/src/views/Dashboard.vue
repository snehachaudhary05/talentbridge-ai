<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">Dashboard</h1>
      <p class="text-xl text-gray-600">Welcome back, {{ authStore.user?.email }}</p>
    </div>

    <!-- Stats Cards -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600">Loading your dashboard...</p>
    </div>

    <!-- Candidate Stats -->
    <div v-else-if="authStore.isCandidate" class="grid md:grid-cols-3 gap-6 mb-8">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">My Applications</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.applications }}</p>
          </div>
          <div class="bg-primary-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Jobs Available</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalJobs }}</p>
          </div>
          <div class="bg-green-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Profile Status</p>
            <p class="text-3xl font-bold text-gray-900">Active</p>
          </div>
          <div class="bg-blue-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recruiter Stats -->
    <div v-else-if="authStore.isRecruiter" class="grid md:grid-cols-4 gap-6 mb-8">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Jobs Posted</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.jobsPosted }}</p>
          </div>
          <div class="bg-primary-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Total Applications</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.applications }}</p>
          </div>
          <div class="bg-green-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Active Jobs</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.activeJobs }}</p>
          </div>
          <div class="bg-purple-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Draft Jobs</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.draftJobs }}</p>
          </div>
          <div class="bg-yellow-100 p-3 rounded-lg">
            <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid md:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div class="space-y-3">
          <!-- Recruiter Actions -->
          <router-link v-if="authStore.isRecruiter" to="/post-job" class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition">
            <svg class="w-6 h-6 text-primary-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            <span class="font-medium text-gray-700">Post a Job</span>
          </router-link>
          <router-link v-if="authStore.isRecruiter" to="/jobs" class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition">
            <svg class="w-6 h-6 text-primary-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <span class="font-medium text-gray-700">My Job Posts</span>
          </router-link>

          <!-- Candidate Actions -->
          <router-link v-if="authStore.isCandidate" to="/jobs" class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition">
            <svg class="w-6 h-6 text-primary-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <span class="font-medium text-gray-700">Browse Jobs</span>
          </router-link>
          <router-link v-if="authStore.isCandidate" to="/ai-assistant" class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition">
            <svg class="w-6 h-6 text-primary-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <span class="font-medium text-gray-700">AI Resume Analysis</span>
          </router-link>

          <!-- Common Actions -->
          <router-link to="/profile" class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition">
            <svg class="w-6 h-6 text-primary-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <span class="font-medium text-gray-700">Update Profile</span>
          </router-link>
        </div>
      </div>

      <!-- Candidates: Recommended Jobs -->
      <div v-if="authStore.isCandidate" class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Recommended Jobs</h2>
        <p class="text-gray-600 mb-4">Based on your profile and preferences</p>
        <router-link to="/jobs" class="btn-primary inline-block">
          View Recommendations
        </router-link>
      </div>

      <!-- Recruiters: Quick Stats -->
      <div v-if="authStore.isRecruiter" class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Hiring Overview</h2>
        <p class="text-gray-600 mb-4">Manage your recruitment process</p>
        <div class="space-y-3">
          <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <span class="text-gray-700">Active Jobs</span>
            <span class="text-2xl font-bold text-primary-600">{{ stats.jobsPosted }}</span>
          </div>
          <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <span class="text-gray-700">Total Applications</span>
            <span class="text-2xl font-bold text-primary-600">{{ stats.applications }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Candidate: My Applications Section -->
    <div v-if="authStore.isCandidate && applications.length > 0" class="card mb-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">My Applications</h2>
      <div class="space-y-4">
        <div v-for="app in applications" :key="app.id" class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
            <div class="flex-1 min-w-0">
              <h3 class="text-base sm:text-lg font-semibold text-gray-900 break-words">{{ app.job_title }}</h3>
              <p class="text-sm text-gray-600 mb-2">{{ app.company_name }}</p>

              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 mt-3">
                <span :class="[
                  'px-3 py-1 rounded-full text-xs sm:text-sm font-medium self-start',
                  app.status === 'applied' ? 'bg-blue-100 text-blue-800' :
                  app.status === 'under_review' ? 'bg-yellow-100 text-yellow-800' :
                  app.status === 'shortlisted' ? 'bg-purple-100 text-purple-800' :
                  app.status === 'oa_round' ? 'bg-indigo-100 text-indigo-800' :
                  app.status === 'tech_round' ? 'bg-cyan-100 text-cyan-800' :
                  app.status === 'hr_round' ? 'bg-teal-100 text-teal-800' :
                  app.status === 'offer_received' ? 'bg-green-100 text-green-800' :
                  app.status === 'accepted' ? 'bg-green-100 text-green-800' :
                  'bg-red-100 text-red-800'
                ]">
                  {{ formatStatus(app.status) }}
                </span>
                <span class="text-sm text-gray-500">
                  Applied {{ formatDate(app.applied_at) }}
                </span>
              </div>

              <!-- Cover Letter Preview -->
              <div v-if="app.cover_letter" class="mt-3 pt-3 border-t border-gray-200">
                <p class="text-sm font-medium text-gray-700 mb-1">Cover Letter:</p>
                <p class="text-sm text-gray-600 line-clamp-2">{{ app.cover_letter }}</p>
              </div>
            </div>

            <div class="sm:ml-4">
              <router-link :to="`/jobs/${app.job}`" class="btn-secondary text-sm block w-full sm:w-auto text-center">
                View Job
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recruiter: Recent Applications Section -->
    <div v-if="authStore.isRecruiter && applications.length > 0" class="card mb-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Recent Applications</h2>
      <div class="space-y-4">
        <div v-for="app in applications" :key="app.id" class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
            <div class="flex-1 min-w-0">
              <h3 class="text-base sm:text-lg font-semibold text-gray-900 break-words">{{ app.candidate_email }}</h3>
              <p class="text-sm text-gray-600 mb-2">Applied for: {{ app.job_title }}</p>

              <!-- Candidate Profile Info (only shown to recruiters who own the job) -->
              <div v-if="app.candidate_profile" class="mt-3 bg-gray-50 p-3 rounded-lg">
                <div class="grid sm:grid-cols-2 gap-2 sm:gap-3 text-sm">
                  <div v-if="app.candidate_profile.skills" class="break-words">
                    <span class="font-medium text-gray-700">Skills:</span>
                    <span class="text-gray-600 ml-2">{{ app.candidate_profile.skills }}</span>
                  </div>
                  <div v-if="app.candidate_profile.location">
                    <span class="font-medium text-gray-700">Location:</span>
                    <span class="text-gray-600 ml-2">{{ app.candidate_profile.location }}</span>
                  </div>
                  <div v-if="app.candidate_profile.experience_years">
                    <span class="font-medium text-gray-700">Experience:</span>
                    <span class="text-gray-600 ml-2">{{ app.candidate_profile.experience_years }} years</span>
                  </div>
                  <div v-if="app.candidate_profile.phone">
                    <span class="font-medium text-gray-700">Phone:</span>
                    <span class="text-gray-600 ml-2">{{ app.candidate_profile.phone }}</span>
                  </div>
                </div>
              </div>

              <div class="flex flex-col sm:flex-row sm:items-center gap-3 mt-3">
                <div>
                  <label class="text-xs font-medium text-gray-700 block mb-1">Status:</label>
                  <select
                    v-model="app.status"
                    @change="updateApplicationStatus(app.id, app.status)"
                    class="text-sm border border-gray-300 rounded-md px-2 py-1 focus:ring-primary-500 focus:border-primary-500 w-full sm:w-auto"
                  >
                    <option value="applied">Applied</option>
                    <option value="under_review">Under Review</option>
                    <option value="shortlisted">Shortlisted</option>
                    <option value="interview_scheduled">Interview Scheduled</option>
                    <option value="rejected">Rejected</option>
                    <option value="accepted">Accepted</option>
                  </select>
                </div>
                <span class="text-sm text-gray-500">
                  Applied {{ formatDate(app.applied_at) }}
                </span>
              </div>
            </div>

            <div class="flex sm:flex-col gap-2 sm:ml-4">
              <!-- Download Resume Button -->
              <button
                v-if="app.candidate_profile?.has_resume"
                @click="downloadResume(app.id)"
                class="btn-secondary text-sm whitespace-nowrap flex-1 sm:flex-none"
              >
                <svg class="w-4 h-4 inline mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Resume
              </button>
              <span v-else class="text-xs text-gray-400 self-center sm:self-start">No resume</span>
            </div>
          </div>

          <!-- Cover Letter -->
          <div v-if="app.cover_letter" class="mt-3 pt-3 border-t border-gray-200">
            <p class="text-sm font-medium text-gray-700 mb-1">Cover Letter:</p>
            <p class="text-sm text-gray-600">{{ app.cover_letter }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const loading = ref(true)
const stats = ref({
  applications: 0,
  jobsPosted: 0,
  totalJobs: 0,
  activeJobs: 0,
  draftJobs: 0
})
const applications = ref([])

const fetchStats = async () => {
  loading.value = true
  try {
    if (authStore.isRecruiter) {
      // Recruiter stats
      const appsResponse = await axios.get('/api/jobs/applications/')
      stats.value.applications = appsResponse.data.length
      applications.value = appsResponse.data.slice(0, 5) // Show latest 5

      const jobsResponse = await axios.get('/api/jobs/jobs/')
      const jobs = jobsResponse.data
      stats.value.jobsPosted = jobs.length
      stats.value.activeJobs = jobs.filter(job => job.status === 'published').length
      stats.value.draftJobs = jobs.filter(job => job.status === 'draft').length
    } else {
      // Candidate stats
      const appsResponse = await axios.get('/api/jobs/applications/')
      stats.value.applications = appsResponse.data.length
      applications.value = appsResponse.data // Store applications for display

      // Fetch total published jobs available for candidates
      const totalJobsResponse = await axios.get('/api/jobs/jobs/')
      stats.value.totalJobs = totalJobsResponse.data.length
    }
  } catch (error) {
    console.error('Error fetching stats:', error)
  } finally {
    loading.value = false
  }
}

const downloadResume = async (applicationId) => {
  try {
    const response = await axios.get(`/api/jobs/applications/${applicationId}/download_resume/`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `candidate_resume.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    alert('Error downloading resume: ' + (error.response?.data?.error || error.message))
  }
}

const updateApplicationStatus = async (applicationId, newStatus) => {
  try {
    await axios.patch(`/api/jobs/applications/${applicationId}/update_status/`, {
      status: newStatus
    })
    alert(`Application status updated to: ${newStatus.replace('_', ' ')}`)
  } catch (error) {
    alert('Error updating status: ' + (error.response?.data?.error || error.message))
    // Reload applications to revert the change
    fetchStats()
  }
}

const getStatusBadgeClass = (status) => {
  const classes = {
    'pending': 'badge-warning',
    'reviewing': 'badge-info',
    'shortlisted': 'badge-primary',
    'interview': 'badge-success',
    'rejected': 'badge-danger',
    'accepted': 'badge-success'
  }
  return classes[status] || 'badge-secondary'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  return date.toLocaleDateString()
}

const formatStatus = (status) => {
  if (!status) return 'N/A'
  return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

onMounted(() => {
  fetchStats()
})
</script>

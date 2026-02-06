<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <button @click="$router.back()" class="flex items-center text-primary-600 hover:text-primary-700 mb-6">
      <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
      </svg>
      Back to jobs
    </button>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="job" class="space-y-6">
      <div class="card">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ job.title }}</h1>
        <p class="text-xl text-gray-700 mb-4">{{ job.company_name }}</p>

        <div class="flex flex-wrap gap-2 mb-6">
          <span class="badge badge-info">{{ formatJobType(job.job_type) }}</span>
          <span v-if="job.is_remote" class="badge badge-success">Remote</span>
          <span class="badge badge-warning">{{ job.status }}</span>
        </div>

        <div class="grid md:grid-cols-2 gap-4 mb-6">
          <div class="flex items-center text-gray-700">
            <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
            </svg>
            {{ job.location }}
          </div>
          <div v-if="job.salary_min" class="flex items-center text-gray-700">
            <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            ${{ job.salary_min }} - ${{ job.salary_max }}
          </div>
        </div>

        <!-- Candidate: Apply Button -->
        <button
          v-if="authStore.isCandidate && !hasApplied"
          class="btn-primary w-full md:w-auto"
          @click="showApplicationModal = true"
        >
          Apply Now
        </button>
        <button
          v-if="authStore.isCandidate && hasApplied"
          class="bg-green-100 text-green-800 px-6 py-2 rounded-lg font-medium cursor-not-allowed w-full md:w-auto"
          disabled
        >
          ✓ Applied
        </button>

        <!-- Recruiter: Job Stats -->
        <div v-if="authStore.isRecruiter && job.recruiter === authStore.user?.id" class="bg-gray-50 rounded-lg p-4 mt-4">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Job Statistics</h3>
          <div class="grid grid-cols-3 gap-4 text-center">
            <div>
              <p class="text-2xl font-bold text-primary-600">{{ job.applications_count || 0 }}</p>
              <p class="text-sm text-gray-600">Applications</p>
            </div>
            <div>
              <p class="text-2xl font-bold text-primary-600">{{ job.views_count || 0 }}</p>
              <p class="text-sm text-gray-600">Views</p>
            </div>
            <div>
              <p class="text-2xl font-bold" :class="job.status === 'published' ? 'text-green-600' : 'text-yellow-600'">
                {{ job.status }}
              </p>
              <p class="text-sm text-gray-600">Status</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Description</h2>
        <p class="text-gray-700 whitespace-pre-line">{{ job.description }}</p>
      </div>

      <div class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Requirements</h2>
        <p class="text-gray-700 whitespace-pre-line">{{ job.requirements }}</p>
      </div>

      <div class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Required Skills</h2>
        <div class="flex flex-wrap gap-2">
          <span v-for="skill in job.required_skills.split(',')" :key="skill" class="badge badge-info">
            {{ skill.trim() }}
          </span>
        </div>
      </div>

      <!-- Recruiter: Applications List -->
      <div v-if="authStore.isRecruiter && job.recruiter === authStore.user?.id && applications.length > 0" class="card">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">
          Applications ({{ applications.length }})
        </h2>
        <div class="space-y-4">
          <div v-for="app in applications" :key="app.id" class="border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900">{{ app.candidate_email }}</h3>
                <p class="text-sm text-gray-600 mb-2">Applied {{ formatDate(app.applied_at) }}</p>

                <!-- Candidate Profile -->
                <div v-if="app.candidate_profile" class="mt-3 bg-gray-50 p-3 rounded-lg">
                  <h4 class="font-semibold text-gray-800 mb-3">Candidate Information</h4>

                  <!-- Name and Contact -->
                  <div class="grid md:grid-cols-2 gap-3 text-sm mb-3">
                    <div v-if="app.candidate_profile.first_name || app.candidate_profile.last_name">
                      <span class="font-medium text-gray-700">Name:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.first_name }} {{ app.candidate_profile.last_name }}</span>
                    </div>
                    <div v-if="app.candidate_profile.email">
                      <span class="font-medium text-gray-700">Email:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.email }}</span>
                    </div>
                    <div v-if="app.candidate_profile.phone">
                      <span class="font-medium text-gray-700">Phone:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.phone }}</span>
                    </div>
                    <div v-if="app.candidate_profile.location">
                      <span class="font-medium text-gray-700">Location:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.location }}</span>
                    </div>
                  </div>

                  <!-- Education -->
                  <div class="grid md:grid-cols-2 gap-3 text-sm mb-3" v-if="app.candidate_profile.college_name || app.candidate_profile.passout_year">
                    <div v-if="app.candidate_profile.college_name">
                      <span class="font-medium text-gray-700">College:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.college_name }}</span>
                    </div>
                    <div v-if="app.candidate_profile.passout_year">
                      <span class="font-medium text-gray-700">Passout Year:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.passout_year }}</span>
                    </div>
                  </div>

                  <!-- Skills and Experience -->
                  <div class="grid md:grid-cols-2 gap-3 text-sm mb-3">
                    <div v-if="app.candidate_profile.skills">
                      <span class="font-medium text-gray-700">Skills:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.skills }}</span>
                    </div>
                    <div v-if="app.candidate_profile.experience_years">
                      <span class="font-medium text-gray-700">Experience:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.experience_years }} years</span>
                    </div>
                  </div>

                  <!-- Social Profiles -->
                  <div class="grid md:grid-cols-3 gap-3 text-sm" v-if="app.candidate_profile.linkedin_url || app.candidate_profile.leetcode_url || app.candidate_profile.github_url">
                    <div v-if="app.candidate_profile.linkedin_url">
                      <span class="font-medium text-gray-700">LinkedIn:</span>
                      <a :href="app.candidate_profile.linkedin_url" target="_blank" class="text-primary-600 hover:underline ml-2 text-xs break-all">
                        View Profile
                      </a>
                    </div>
                    <div v-if="app.candidate_profile.leetcode_url">
                      <span class="font-medium text-gray-700">LeetCode:</span>
                      <a :href="app.candidate_profile.leetcode_url" target="_blank" class="text-primary-600 hover:underline ml-2 text-xs break-all">
                        View Profile
                      </a>
                    </div>
                    <div v-if="app.candidate_profile.github_url">
                      <span class="font-medium text-gray-700">GitHub:</span>
                      <a :href="app.candidate_profile.github_url" target="_blank" class="text-primary-600 hover:underline ml-2 text-xs break-all">
                        View Profile
                      </a>
                    </div>
                  </div>
                </div>

                <div class="mt-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Status:</label>
                  <select
                    v-model="app.status"
                    @change="updateApplicationStatus(app.id, app.status)"
                    class="block w-48 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                    <option value="applied">Applied</option>
                    <option value="under_review">Under Review</option>
                    <option value="shortlisted">Shortlisted</option>
                    <option value="oa_round">OA Round</option>
                    <option value="tech_round">Tech Round</option>
                    <option value="hr_round">HR Round</option>
                    <option value="offer_received">Offer Received</option>
                    <option value="rejected">Rejected</option>
                    <option value="accepted">Accepted</option>
                  </select>
                </div>
              </div>

              <div class="flex flex-col gap-2">
                <!-- Download Resume Button -->
                <button
                  v-if="app.candidate_profile?.has_resume"
                  @click="downloadResume(app.id)"
                  class="btn-secondary text-sm"
                >
                  Download Resume
                </button>
              </div>
            </div>

            <div v-if="app.cover_letter" class="mt-3 pt-3 border-t border-gray-200">
              <p class="text-sm font-medium text-gray-700 mb-1">Cover Letter:</p>
              <p class="text-sm text-gray-600">{{ app.cover_letter }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recruiter: No Applications -->
      <div v-if="authStore.isRecruiter && job.recruiter === authStore.user?.id && applications.length === 0" class="card text-center py-8">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
        </svg>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No Applications Yet</h3>
        <p class="text-gray-600">This job hasn't received any applications</p>
      </div>
    </div>

    <!-- Application Modal -->
    <ApplicationModal
      :show="showApplicationModal"
      :job-id="job?.id"
      :job-title="job?.title"
      @close="showApplicationModal = false"
      @success="handleApplicationSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ApplicationModal from '../components/ApplicationModal.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const job = ref(null)
const loading = ref(true)
const applications = ref([])
const showApplicationModal = ref(false)
const hasApplied = ref(false)

const fetchJob = async () => {
  try {
    const response = await axios.get(`/api/jobs/jobs/${route.params.id}/`)
    job.value = response.data

    // Fetch applications if recruiter owns this job
    if (authStore.isRecruiter && job.value.recruiter === authStore.user?.id) {
      await fetchApplications()
    }

    // Check if candidate has already applied
    if (authStore.isCandidate) {
      await checkIfApplied()
    }
  } catch (error) {
    console.error('Error fetching job:', error)
  } finally {
    loading.value = false
  }
}

const checkIfApplied = async () => {
  try {
    const response = await axios.get('/jobs/applications/')
    hasApplied.value = response.data.some(app => app.job === job.value.id)
  } catch (error) {
    console.error('Error checking application status:', error)
  }
}

const fetchApplications = async () => {
  try {
    const response = await axios.get(`/api/jobs/jobs/${route.params.id}/applications/`)
    applications.value = response.data
  } catch (error) {
    console.error('Error fetching applications:', error)
  }
}

const handleApplicationSuccess = () => {
  alert('Application submitted successfully!')
  hasApplied.value = true
  // Refresh job details to update application count if needed
  fetchJob()
}

const formatJobType = (type) => {
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
  return date.toLocaleDateString()
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
    alert('Application status updated successfully!')
  } catch (error) {
    alert('Error updating status: ' + (error.response?.data?.error || error.message))
    // Refresh to revert the change if it failed
    fetchApplications()
  }
}

onMounted(() => {
  fetchJob()
})
</script>

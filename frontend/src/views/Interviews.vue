<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">My Interviews</h1>
      <p class="text-xl text-gray-600">
        {{ authStore.isRecruiter ? 'Manage your scheduled interviews with candidates' : 'View your upcoming and past interviews' }}
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-gray-600">Loading interviews...</p>
    </div>

    <!-- Content -->
    <div v-else>
      <!-- Tabs -->
      <div class="mb-6 border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button
            @click="activeTab = 'upcoming'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'upcoming'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Upcoming ({{ upcomingInterviews.length }})
          </button>
          <button
            @click="activeTab = 'past'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'past'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Past & Cancelled ({{ pastInterviews.length }})
          </button>
          <button
            v-if="authStore.isRecruiter"
            @click="activeTab = 'applications'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'applications'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            All Applications ({{ applications.length }})
          </button>
        </nav>
      </div>

      <!-- Upcoming Interviews -->
      <div v-if="activeTab === 'upcoming'">
        <div v-if="upcomingInterviews.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">No upcoming interviews</h3>
          <p class="mt-1 text-gray-500">
            {{ authStore.isRecruiter ? 'Schedule interviews with candidates from your dashboard' : 'Your upcoming interviews will appear here' }}
          </p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="interview in upcomingInterviews"
            :key="interview.id"
            class="card hover:shadow-lg transition-shadow"
          >
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
              <div class="flex-1 min-w-0">
                <!-- Header -->
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 sm:gap-3 mb-3">
                  <div class="flex-1 min-w-0">
                    <h3 class="text-base sm:text-xl font-semibold text-gray-900 break-words">{{ interview.job_title }}</h3>
                    <p class="text-sm text-gray-600">{{ interview.company_name }}</p>
                  </div>
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs sm:text-sm font-medium self-start',
                    interview.status === 'scheduled' ? 'bg-green-100 text-green-800' :
                    interview.status === 'rescheduled' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ formatStatus(interview.status) }}
                  </span>
                </div>

                <!-- Candidate/Recruiter Info -->
                <div class="mb-3">
                  <p class="text-sm font-medium text-gray-700">
                    {{ authStore.isRecruiter ? 'Candidate' : 'Interviewer' }}:
                  </p>
                  <p class="text-sm sm:text-base text-gray-900 break-words">
                    {{ authStore.isRecruiter ? interview.candidate_name : interview.recruiter_email }}
                  </p>
                  <p v-if="authStore.isRecruiter" class="text-sm text-gray-600 break-words">
                    {{ interview.candidate_email }}
                  </p>
                </div>

                <!-- Interview Details -->
                <div class="grid sm:grid-cols-2 gap-3 sm:gap-4 bg-gray-50 p-3 sm:p-4 rounded-lg">
                  <div>
                    <p class="text-sm font-medium text-gray-700 mb-1">
                      <svg class="w-4 h-4 inline mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                      Date & Time
                    </p>
                    <p class="text-sm sm:text-base text-gray-900 break-words">{{ formatDateTime(interview.scheduled_datetime) }}</p>
                    <p class="text-sm text-gray-600">Duration: {{ interview.duration_minutes }} minutes</p>
                  </div>

                  <div>
                    <p class="text-sm font-medium text-gray-700 mb-1">
                      <svg class="w-4 h-4 inline mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                      </svg>
                      Interview Type
                    </p>
                    <p class="text-sm sm:text-base text-gray-900">{{ formatInterviewType(interview.interview_type) }}</p>
                  </div>

                  <div class="sm:col-span-2">
                    <p class="text-sm font-medium text-gray-700 mb-1">
                      <svg class="w-4 h-4 inline mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                      </svg>
                      {{ interview.interview_type === 'in_person' ? 'Location' : 'Meeting Link' }}
                    </p>
                    <p class="text-sm sm:text-base text-gray-900 break-all">{{ interview.location }}</p>
                    <a
                      v-if="interview.interview_type !== 'in_person' && interview.location.includes('http')"
                      :href="interview.location"
                      target="_blank"
                      class="text-primary-600 hover:text-primary-700 text-sm mt-1 inline-block break-all"
                    >
                      Join Meeting →
                    </a>
                  </div>

                  <div v-if="interview.notes" class="sm:col-span-2">
                    <p class="text-sm font-medium text-gray-700 mb-1">Additional Notes</p>
                    <p class="text-sm text-gray-600 break-words">{{ interview.notes }}</p>
                  </div>
                </div>
              </div>

              <!-- Actions (Recruiter Only) -->
              <div v-if="authStore.isRecruiter" class="sm:ml-4">
                <button
                  @click="cancelInterview(interview)"
                  class="px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors text-sm w-full sm:w-auto"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Past & Cancelled Interviews -->
      <div v-if="activeTab === 'past'">
        <div v-if="pastInterviews.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">No past interviews</h3>
          <p class="mt-1 text-gray-500">Your interview history will appear here</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="interview in pastInterviews"
            :key="interview.id"
            class="card opacity-75"
          >
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
              <div class="flex-1 min-w-0">
                <!-- Header -->
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 sm:gap-3 mb-3">
                  <div class="flex-1 min-w-0">
                    <h3 class="text-base sm:text-xl font-semibold text-gray-900 break-words">{{ interview.job_title }}</h3>
                    <p class="text-sm text-gray-600">{{ interview.company_name }}</p>
                  </div>
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs sm:text-sm font-medium self-start',
                    interview.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                    interview.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ formatStatus(interview.status) }}
                  </span>
                </div>

                <!-- Candidate/Recruiter Info -->
                <div class="mb-3">
                  <p class="text-sm font-medium text-gray-700">
                    {{ authStore.isRecruiter ? 'Candidate' : 'Interviewer' }}:
                  </p>
                  <p class="text-sm sm:text-base text-gray-900 break-words">
                    {{ authStore.isRecruiter ? interview.candidate_name : interview.recruiter_email }}
                  </p>
                </div>

                <!-- Interview Details -->
                <div class="bg-gray-50 p-3 sm:p-4 rounded-lg">
                  <p class="text-sm text-gray-600 break-words">
                    <strong>Date:</strong> {{ formatDateTime(interview.scheduled_datetime) }}
                  </p>
                  <p class="text-sm text-gray-600">
                    <strong>Type:</strong> {{ formatInterviewType(interview.interview_type) }}
                  </p>
                  <p v-if="interview.notes" class="text-sm text-gray-600 mt-2 break-words">
                    <strong>Notes:</strong> {{ interview.notes }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- All Applications Tab (Recruiter Only) -->
      <div v-if="activeTab === 'applications' && authStore.isRecruiter">
        <div v-if="applications.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">No applications yet</h3>
          <p class="mt-1 text-gray-500">Applications will appear here when candidates apply to your jobs</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="app in applications"
            :key="app.id"
            class="card hover:shadow-lg transition-shadow"
          >
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
              <div class="flex-1 min-w-0">
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 sm:gap-3 mb-3">
                  <div class="flex-1 min-w-0">
                    <h3 class="text-base sm:text-xl font-semibold text-gray-900 break-words">
                      {{ app.candidate_profile?.first_name }} {{ app.candidate_profile?.last_name }}
                    </h3>
                    <p class="text-sm text-gray-600 break-words">{{ app.candidate_email }}</p>
                  </div>
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs sm:text-sm font-medium self-start',
                    app.status === 'applied' ? 'bg-blue-100 text-blue-800' :
                    app.status === 'under_review' ? 'bg-yellow-100 text-yellow-800' :
                    app.status === 'shortlisted' ? 'bg-purple-100 text-purple-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ formatStatus(app.status) }}
                  </span>
                </div>

                <div class="mb-3">
                  <p class="text-sm font-medium text-gray-700">Applied for:</p>
                  <p class="text-sm sm:text-base text-gray-900 break-words">{{ app.job_title }} - {{ app.company_name }}</p>
                </div>

                <div v-if="app.candidate_profile" class="bg-gray-50 p-3 rounded-lg mb-3">
                  <div class="grid sm:grid-cols-2 gap-2 sm:gap-3 text-sm">
                    <div v-if="app.candidate_profile.skills" class="break-words">
                      <span class="font-medium text-gray-700">Skills:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.skills }}</span>
                    </div>
                    <div v-if="app.candidate_profile.experience_years">
                      <span class="font-medium text-gray-700">Experience:</span>
                      <span class="text-gray-600 ml-2">{{ app.candidate_profile.experience_years }} years</span>
                    </div>
                  </div>
                </div>

                <p class="text-sm text-gray-500">Applied {{ formatDate(app.applied_at) }}</p>
              </div>

              <div class="sm:ml-4">
                <button
                  @click="openScheduleModal(app)"
                  class="btn-primary text-sm whitespace-nowrap w-full sm:w-auto"
                >
                  <svg class="w-4 h-4 inline mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  Schedule Interview
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Schedule Interview Modal -->
    <ScheduleInterviewModal
      v-if="selectedApplication"
      :is-open="showScheduleModal"
      :application="selectedApplication"
      @close="closeScheduleModal"
      @scheduled="handleInterviewScheduled"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import ScheduleInterviewModal from '../components/ScheduleInterviewModal.vue'
import axios from 'axios'

const authStore = useAuthStore()
const loading = ref(true)
const interviews = ref([])
const activeTab = ref('upcoming')
const applications = ref([])
const showScheduleModal = ref(false)
const selectedApplication = ref(null)

const upcomingInterviews = computed(() => {
  const now = new Date()
  return interviews.value.filter(interview => {
    const interviewDate = new Date(interview.scheduled_datetime)
    return interviewDate >= now && interview.status === 'scheduled'
  }).sort((a, b) => new Date(a.scheduled_datetime) - new Date(b.scheduled_datetime))
})

const pastInterviews = computed(() => {
  const now = new Date()
  return interviews.value.filter(interview => {
    const interviewDate = new Date(interview.scheduled_datetime)
    return interviewDate < now || interview.status === 'cancelled' || interview.status === 'completed'
  }).sort((a, b) => new Date(b.scheduled_datetime) - new Date(a.scheduled_datetime))
})

const fetchInterviews = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/jobs/interviews/')
    interviews.value = response.data

    // Fetch applications for recruiters
    if (authStore.isRecruiter) {
      await fetchApplications()
    }
  } catch (error) {
    console.error('Error fetching interviews:', error)
    alert('Failed to load interviews')
  } finally {
    loading.value = false
  }
}

const fetchApplications = async () => {
  try {
    const response = await axios.get('/api/jobs/applications/')
    applications.value = response.data
  } catch (error) {
    console.error('Error fetching applications:', error)
  }
}

const openScheduleModal = (application = null) => {
  selectedApplication.value = application
  showScheduleModal.value = true
}

const closeScheduleModal = () => {
  showScheduleModal.value = false
  selectedApplication.value = null
}

const handleInterviewScheduled = () => {
  // Refresh interviews after scheduling
  fetchInterviews()
  alert('Interview scheduled successfully! The candidate will receive an email notification.')
}

const cancelInterview = async (interview) => {
  if (!confirm(`Are you sure you want to cancel the interview with ${interview.candidate_name}?`)) {
    return
  }

  try {
    await axios.post(`/api/jobs/interviews/${interview.id}/cancel/`)
    alert('Interview cancelled successfully. The candidate will be notified.')
    fetchInterviews()
  } catch (error) {
    console.error('Error cancelling interview:', error)
    alert('Failed to cancel interview: ' + (error.response?.data?.error || error.message))
  }
}

const formatDateTime = (dateTimeString) => {
  const date = new Date(dateTimeString)
  const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
  const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true }

  const formattedDate = date.toLocaleDateString('en-US', dateOptions)
  const formattedTime = date.toLocaleTimeString('en-US', timeOptions)

  return `${formattedDate} at ${formattedTime}`
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

const formatInterviewType = (type) => {
  const types = {
    'phone': 'Phone Interview',
    'video': 'Video Interview',
    'in_person': 'In-Person Interview'
  }
  return types[type] || type
}

const formatStatus = (status) => {
  return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

onMounted(() => {
  fetchInterviews()
})
</script>

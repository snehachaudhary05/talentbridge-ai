<template>
  <div v-if="show" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="closeModal">
    <div class="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-2xl font-bold text-gray-900">Apply for {{ jobTitle }}</h3>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitApplication" class="space-y-4">
        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          <p class="font-semibold">Error:</p>
          <p class="text-sm">{{ error }}</p>
        </div>

        <!-- Personal Information -->
        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">First Name *</label>
            <input v-model="form.first_name" type="text" required class="input-field" placeholder="John">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Last Name *</label>
            <input v-model="form.last_name" type="text" required class="input-field" placeholder="Doe">
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" disabled class="input-field bg-gray-100" />
          <p class="text-xs text-gray-500 mt-1">This is your registered email</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
          <input v-model="form.phone" type="tel" class="input-field" placeholder="+1 234 567 8900">
        </div>

        <!-- Education -->
        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">College/University</label>
            <input v-model="form.college_name" type="text" class="input-field" placeholder="MIT">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Passout Year</label>
            <input v-model.number="form.passout_year" type="number" class="input-field" placeholder="2024" min="1950" :max="new Date().getFullYear() + 10">
          </div>
        </div>

        <!-- Resume Upload -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Upload Resume * (PDF, DOC, DOCX)</label>
          <input @change="handleFileChange" type="file" accept=".pdf,.doc,.docx" class="input-field" required>
          <p v-if="form.resume" class="text-sm text-green-600 mt-1">✓ {{ form.resume.name }}</p>
        </div>

        <!-- Social Profiles -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">LinkedIn Profile</label>
          <input v-model="form.linkedin_url" type="url" class="input-field" placeholder="https://linkedin.com/in/yourprofile">
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">LeetCode Profile</label>
            <input v-model="form.leetcode_url" type="url" class="input-field" placeholder="https://leetcode.com/yourprofile">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">GitHub Profile</label>
            <input v-model="form.github_url" type="url" class="input-field" placeholder="https://github.com/yourprofile">
          </div>
        </div>

        <!-- Cover Letter -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Cover Letter (Optional)</label>
          <textarea v-model="form.cover_letter" rows="4" class="input-field" placeholder="Tell us why you're a great fit for this role..."></textarea>
        </div>

        <!-- Submit Buttons -->
        <div class="flex gap-3 pt-4">
          <button type="submit" :disabled="submitting" class="btn-primary flex-1">
            {{ submitting ? 'Submitting...' : 'Submit Application' }}
          </button>
          <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const props = defineProps({
  show: Boolean,
  jobId: Number,
  jobTitle: String
})

const emit = defineEmits(['close', 'success'])

const authStore = useAuthStore()
const submitting = ref(false)
const error = ref('')

const form = ref({
  email: authStore.user?.email || '',
  first_name: '',
  last_name: '',
  phone: '',
  college_name: '',
  passout_year: null,
  linkedin_url: '',
  leetcode_url: '',
  github_url: '',
  resume: null,
  cover_letter: ''
})

// Watch for modal show/hide to reset form
watch(() => props.show, (newVal) => {
  if (newVal) {
    loadCandidateProfile()
  } else {
    error.value = ''
  }
})

const loadCandidateProfile = async () => {
  try {
    const response = await axios.get('/accounts/profile/')
    if (response.data.length > 0) {
      const profile = response.data[0]
      form.value.first_name = profile.first_name || ''
      form.value.last_name = profile.last_name || ''
      form.value.phone = profile.phone || ''
      form.value.college_name = profile.college_name || ''
      form.value.passout_year = profile.passout_year || null
      form.value.linkedin_url = profile.linkedin_url || ''
      form.value.leetcode_url = profile.leetcode_url || ''
      form.value.github_url = profile.github_url || ''
    }
  } catch (err) {
    console.error('Error loading profile:', err)
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      error.value = 'File size must be less than 5MB'
      event.target.value = ''
      return
    }
    form.value.resume = file
  }
}

const submitApplication = async () => {
  submitting.value = true
  error.value = ''

  try {
    const formData = new FormData()
    formData.append('job', props.jobId)
    formData.append('first_name', form.value.first_name)
    formData.append('last_name', form.value.last_name)

    if (form.value.phone) formData.append('phone', form.value.phone)
    if (form.value.college_name) formData.append('college_name', form.value.college_name)
    if (form.value.passout_year) formData.append('passout_year', form.value.passout_year)
    if (form.value.linkedin_url) formData.append('linkedin_url', form.value.linkedin_url)
    if (form.value.leetcode_url) formData.append('leetcode_url', form.value.leetcode_url)
    if (form.value.github_url) formData.append('github_url', form.value.github_url)
    if (form.value.cover_letter) formData.append('cover_letter', form.value.cover_letter)
    if (form.value.resume) formData.append('resume', form.value.resume)

    await axios.post('/jobs/applications/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    emit('success')
    closeModal()
  } catch (err) {
    if (err.response?.data) {
      if (typeof err.response.data === 'object') {
        const errorMessages = Object.entries(err.response.data)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('\n')
        error.value = errorMessages
      } else {
        error.value = err.response.data.toString()
      }
    } else {
      error.value = err.message || 'An error occurred while submitting your application'
    }
  } finally {
    submitting.value = false
  }
}

const closeModal = () => {
  emit('close')
}
</script>

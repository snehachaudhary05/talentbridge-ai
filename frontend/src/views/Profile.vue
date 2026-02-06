<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">Profile Settings</h1>
      <p class="text-xl text-gray-600">Manage your account and resume</p>
    </div>

    <!-- Profile Info Card -->
    <div class="card mb-6">
      <div class="flex items-center mb-8">
        <div class="w-16 h-16 sm:w-20 sm:h-20 bg-primary-100 rounded-full flex items-center justify-center text-2xl sm:text-3xl font-bold text-primary-600 flex-shrink-0">
          {{ authStore.user?.email?.[0].toUpperCase() }}
        </div>
        <div class="ml-4 sm:ml-6 min-w-0 flex-1">
          <h2 class="text-lg sm:text-2xl font-bold text-gray-900 break-words">{{ authStore.user?.email }}</h2>
          <p class="text-sm sm:text-base text-gray-600 capitalize">{{ authStore.user?.role }}</p>
        </div>
      </div>

      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input type="email" :value="authStore.user?.email" disabled class="input-field bg-gray-50" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Role</label>
          <input type="text" :value="authStore.user?.role" disabled class="input-field bg-gray-50 capitalize" />
        </div>
      </div>
    </div>

    <!-- Resume Upload Section (Candidates Only) -->
    <div v-if="authStore.isCandidate" class="card mb-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Resume Management</h2>

      <!-- Current Resume -->
      <div v-if="profile?.resume_url" class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <svg class="w-8 h-8 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <div>
              <p class="font-semibold text-gray-900">Resume Uploaded</p>
              <p class="text-sm text-gray-600">Last updated: {{ formatDate(profile.updated_at) }}</p>
            </div>
          </div>
          <button @click="downloadResume" class="btn-secondary">
            Download
          </button>
        </div>
      </div>

      <!-- Upload Form -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ profile?.resume_url ? 'Replace Resume' : 'Upload Resume' }}
        </label>
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-500 transition">
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.doc,.docx"
            @change="handleFileSelect"
            class="hidden"
          />
          <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
          <p class="text-gray-700 font-medium mb-2">
            {{ selectedFile ? selectedFile.name : 'Click to upload or drag and drop' }}
          </p>
          <p class="text-sm text-gray-500 mb-4">PDF, DOC, or DOCX (Max 5MB)</p>
          <button @click="triggerFileInput" class="btn-primary">
            {{ selectedFile ? 'Change File' : 'Select Resume' }}
          </button>
        </div>

        <button
          v-if="selectedFile"
          @click="uploadResume"
          :disabled="uploading"
          class="btn-primary w-full mt-4"
        >
          {{ uploading ? 'Uploading...' : 'Upload Resume' }}
        </button>
      </div>

      <!-- Additional Profile Fields -->
      <div class="mt-8 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Skills</label>
          <input
            v-model="profileForm.skills"
            type="text"
            class="input-field"
            placeholder="Python, Django, React, PostgreSQL..."
          />
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
            <input
              v-model="profileForm.phone"
              type="tel"
              class="input-field"
              placeholder="+1 (555) 123-4567"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input
              v-model="profileForm.location"
              type="text"
              class="input-field"
              placeholder="San Francisco, CA"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
          <input
            v-model.number="profileForm.experience_years"
            type="number"
            class="input-field"
            placeholder="5"
          />
        </div>

        <button @click="updateProfile" :disabled="updating" class="btn-primary">
          {{ updating ? 'Saving...' : 'Save Profile' }}
        </button>
      </div>
    </div>

    <!-- Account Actions -->
    <div class="card">
      <h3 class="text-lg font-bold text-gray-900 mb-4">Account Actions</h3>
      <div class="space-y-3">
        <button @click="handleLogout" class="btn-secondary w-full md:w-auto text-red-600 border-red-300 hover:bg-red-50">
          Sign Out
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

const authStore = useAuthStore()
const router = useRouter()

const fileInput = ref(null)
const selectedFile = ref(null)
const uploading = ref(false)
const updating = ref(false)
const profile = ref(null)

const profileForm = ref({
  skills: '',
  phone: '',
  location: '',
  experience_years: null
})

const fetchProfile = async () => {
  if (!authStore.isCandidate) return

  try {
    const response = await axios.get('/api/accounts/profile/me/')
    profile.value = response.data

    // Populate form
    profileForm.value = {
      skills: profile.value.skills || '',
      phone: profile.value.phone || '',
      location: profile.value.location || '',
      experience_years: profile.value.experience_years || null
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && file.size <= 5 * 1024 * 1024) { // 5MB limit
    selectedFile.value = file
  } else {
    alert('File must be less than 5MB')
  }
}

const uploadResume = async () => {
  if (!selectedFile.value) return

  uploading.value = true
  const formData = new FormData()
  formData.append('resume_file', selectedFile.value)

  // Add profile fields
  Object.keys(profileForm.value).forEach(key => {
    if (profileForm.value[key]) {
      formData.append(key, profileForm.value[key])
    }
  })

  try {
    const response = await axios.post('/api/accounts/profile/upload_resume/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    profile.value = response.data
    selectedFile.value = null
    alert('Resume uploaded successfully!')
    await fetchProfile()
  } catch (error) {
    alert('Error uploading resume: ' + (error.response?.data?.error || error.message))
  } finally {
    uploading.value = false
  }
}

const updateProfile = async () => {
  updating.value = true
  try {
    const response = await axios.patch(`/api/accounts/profile/${profile.value.id}/`, profileForm.value)
    profile.value = response.data
    alert('Profile updated successfully!')
  } catch (error) {
    alert('Error updating profile: ' + error.message)
  } finally {
    updating.value = false
  }
}

const downloadResume = async () => {
  try {
    const response = await axios.get('/api/accounts/profile/download_resume/', {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'resume.pdf')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    alert('Error downloading resume: ' + error.message)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchProfile()
})
</script>

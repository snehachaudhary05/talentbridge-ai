<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Schedule Interview</h2>
          <p class="text-sm text-gray-600 mt-1">
            {{ application.candidate_profile?.first_name }} {{ application.candidate_profile?.last_name }} - {{ application.job_title }}
          </p>
        </div>
        <button
          @click="closeModal"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- Date and Time -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="date" class="block text-sm font-medium text-gray-700 mb-2">
              Date <span class="text-red-500">*</span>
            </label>
            <input
              id="date"
              v-model="formData.date"
              type="date"
              required
              :min="today"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label for="time" class="block text-sm font-medium text-gray-700 mb-2">
              Time <span class="text-red-500">*</span>
            </label>
            <input
              id="time"
              v-model="formData.time"
              type="time"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <!-- Duration -->
        <div>
          <label for="duration" class="block text-sm font-medium text-gray-700 mb-2">
            Duration <span class="text-red-500">*</span>
          </label>
          <select
            id="duration"
            v-model="formData.duration_minutes"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="30">30 minutes</option>
            <option value="60">1 hour</option>
            <option value="90">1.5 hours</option>
            <option value="120">2 hours</option>
          </select>
        </div>

        <!-- Interview Type -->
        <div>
          <label for="type" class="block text-sm font-medium text-gray-700 mb-2">
            Interview Type <span class="text-red-500">*</span>
          </label>
          <select
            id="type"
            v-model="formData.interview_type"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="phone">Phone Interview</option>
            <option value="video">Video Interview</option>
            <option value="in_person">In-Person Interview</option>
          </select>
        </div>

        <!-- Location / Meeting Link -->
        <div>
          <label for="location" class="block text-sm font-medium text-gray-700 mb-2">
            {{ formData.interview_type === 'in_person' ? 'Location' : 'Meeting Link' }}
            <span class="text-red-500">*</span>
          </label>
          <input
            id="location"
            v-model="formData.location"
            type="text"
            required
            :placeholder="formData.interview_type === 'in_person' ? 'Enter office address' : 'Enter video call link (Zoom, Google Meet, etc.)'"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <!-- Notes -->
        <div>
          <label for="notes" class="block text-sm font-medium text-gray-700 mb-2">
            Additional Notes (Optional)
          </label>
          <textarea
            id="notes"
            v-model="formData.notes"
            rows="4"
            placeholder="Add any additional information for the candidate..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          ></textarea>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-4 border-t">
          <button
            type="button"
            @click="closeModal"
            class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            :disabled="loading"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
            :disabled="loading"
          >
            <svg v-if="loading" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Scheduling...' : 'Schedule Interview' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  application: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'scheduled'])

const loading = ref(false)
const error = ref('')

const formData = ref({
  date: '',
  time: '',
  duration_minutes: 60,
  interview_type: 'video',
  location: '',
  notes: ''
})

// Get today's date in YYYY-MM-DD format for min date
const today = computed(() => {
  const date = new Date()
  return date.toISOString().split('T')[0]
})

const closeModal = () => {
  if (!loading.value) {
    error.value = ''
    formData.value = {
      date: '',
      time: '',
      duration_minutes: 60,
      interview_type: 'video',
      location: '',
      notes: ''
    }
    emit('close')
  }
}

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''

    // Combine date and time into ISO datetime string
    const scheduledDatetime = new Date(`${formData.value.date}T${formData.value.time}`)

    // Validate datetime is in the future
    if (scheduledDatetime <= new Date()) {
      error.value = 'Interview must be scheduled for a future date and time'
      loading.value = false
      return
    }

    const payload = {
      application: props.application.id,
      scheduled_datetime: scheduledDatetime.toISOString(),
      duration_minutes: parseInt(formData.value.duration_minutes),
      interview_type: formData.value.interview_type,
      location: formData.value.location,
      notes: formData.value.notes,
      status: 'scheduled'
    }

    await axios.post('/jobs/interviews/', payload)

    // Success - emit event and close modal
    emit('scheduled')
    closeModal()
  } catch (err) {
    console.error('Error scheduling interview:', err)
    if (err.response?.data) {
      // Handle specific error messages from backend
      if (typeof err.response.data === 'object') {
        const errors = Object.entries(err.response.data)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('; ')
        error.value = errors || 'Failed to schedule interview'
      } else {
        error.value = err.response.data
      }
    } else {
      error.value = 'Failed to schedule interview. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">Post a Job</h1>
      <p class="text-xl text-gray-600">Fill in the details to create a new job posting</p>
    </div>

    <!-- Job Form -->
    <div class="card">
      <!-- Error Message -->
      <div v-if="error" class="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
        <p class="font-semibold">Error posting job:</p>
        <p class="text-sm mt-1">{{ error }}</p>
      </div>

      <form @submit.prevent="submitJob" class="space-y-6">
        <!-- Basic Information -->
        <div>
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Basic Information</h2>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Job Title *</label>
              <input
                v-model="jobForm.title"
                type="text"
                required
                class="input-field"
                placeholder="e.g., Senior Full Stack Developer"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Company Name *</label>
              <input
                v-model="jobForm.company_name"
                type="text"
                required
                class="input-field"
                placeholder="e.g., Google Inc."
              />
            </div>

            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Job Type *</label>
                <select v-model="jobForm.job_type" required class="input-field">
                  <option value="">Select Type</option>
                  <option value="full_time">Full Time</option>
                  <option value="part_time">Part Time</option>
                  <option value="contract">Contract</option>
                  <option value="internship">Internship</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Location *</label>
                <input
                  v-model="jobForm.location"
                  type="text"
                  required
                  class="input-field"
                  placeholder="e.g., San Francisco, CA"
                />
              </div>
            </div>

            <div class="flex items-center">
              <input
                v-model="jobForm.is_remote"
                type="checkbox"
                id="is_remote"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <label for="is_remote" class="ml-2 text-sm text-gray-700">Remote position</label>
            </div>
          </div>
        </div>

        <!-- Job Details -->
        <div>
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Job Details</h2>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
              <textarea
                v-model="jobForm.description"
                required
                rows="5"
                class="input-field"
                placeholder="Provide a detailed description of the role..."
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Requirements *</label>
              <textarea
                v-model="jobForm.requirements"
                required
                rows="4"
                class="input-field"
                placeholder="List the key requirements for this position..."
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Responsibilities</label>
              <textarea
                v-model="jobForm.responsibilities"
                rows="4"
                class="input-field"
                placeholder="Describe the main responsibilities..."
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Required Skills *</label>
              <input
                v-model="jobForm.required_skills"
                type="text"
                required
                class="input-field"
                placeholder="e.g., Python, Django, React, PostgreSQL"
              />
              <p class="text-sm text-gray-500 mt-1">Separate skills with commas</p>
            </div>
          </div>
        </div>

        <!-- Compensation & Experience -->
        <div>
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Compensation & Experience</h2>

          <div class="space-y-4">
            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Minimum Salary ($)</label>
                <input
                  v-model.number="jobForm.salary_min"
                  type="number"
                  class="input-field"
                  placeholder="e.g., 50000"
                  min="0"
                  step="1000"
                />
                <p class="text-sm text-gray-500 mt-1">Annual salary in USD</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Maximum Salary ($)</label>
                <input
                  v-model.number="jobForm.salary_max"
                  type="number"
                  class="input-field"
                  placeholder="e.g., 100000"
                  min="0"
                  step="1000"
                />
                <p class="text-sm text-gray-500 mt-1">Annual salary in USD</p>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Required Experience (years)
              </label>
              <input
                v-model.number="jobForm.required_experience"
                type="number"
                class="input-field"
                placeholder="e.g., 3"
                min="0"
                max="50"
                step="1"
              />
              <p class="text-sm text-gray-500 mt-1">Leave blank if no experience required</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Application Deadline (Optional)
              </label>
              <input
                v-model="jobForm.deadline"
                type="date"
                class="input-field"
                :min="new Date().toISOString().split('T')[0]"
              />
              <p class="text-sm text-gray-500 mt-1">Last date for accepting applications</p>
            </div>
          </div>
        </div>

        <!-- Status -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
          <select v-model="jobForm.status" class="input-field">
            <option value="draft">Draft (not visible to candidates)</option>
            <option value="published">Published (visible to candidates)</option>
          </select>
        </div>

        <!-- Submit Buttons -->
        <div class="flex gap-3">
          <button
            type="submit"
            :disabled="submitting"
            class="btn-primary"
          >
            {{ submitting ? 'Posting...' : 'Post Job' }}
          </button>
          <button
            type="button"
            @click="$router.push('/dashboard')"
            class="btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const submitting = ref(false)
const error = ref('')
const jobForm = ref({
  title: '',
  company_name: '',
  description: '',
  requirements: '',
  responsibilities: '',
  job_type: '',
  location: '',
  is_remote: false,
  salary_min: null,
  salary_max: null,
  required_skills: '',
  required_experience: null,
  deadline: '',
  status: 'published'
})

const submitJob = async () => {
  submitting.value = true
  error.value = ''

  // Client-side validation
  if (!jobForm.value.title || !jobForm.value.company_name || !jobForm.value.job_type) {
    error.value = 'Please fill in all required fields (Title, Company Name, Job Type)'
    submitting.value = false
    return
  }

  if (jobForm.value.salary_min && jobForm.value.salary_max && jobForm.value.salary_min > jobForm.value.salary_max) {
    error.value = 'Minimum salary cannot be greater than maximum salary'
    submitting.value = false
    return
  }

  if (jobForm.value.required_experience && jobForm.value.required_experience < 0) {
    error.value = 'Required experience must be 0 or greater'
    submitting.value = false
    return
  }

  try {
    const response = await axios.post('/api/jobs/jobs/', jobForm.value)
    alert('Job posted successfully!')
    router.push('/dashboard')
  } catch (err) {
    if (err.response?.data) {
      // Handle backend validation errors
      const errors = err.response.data
      if (typeof errors === 'object') {
        const errorMessages = Object.entries(errors)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('\n')
        error.value = errorMessages
      } else {
        error.value = errors.toString()
      }
    } else {
      error.value = err.message || 'An error occurred while posting the job'
    }
    console.error('Error:', err.response?.data)
  } finally {
    submitting.value = false
  }
}
</script>

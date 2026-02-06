<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">AI Assistant</h1>
      <p class="text-xl text-gray-600">
        {{ authStore.isRecruiter ? 'AI-powered tools for recruitment' : 'Get AI-powered insights for your job search' }}
      </p>
    </div>

    <!-- Candidate Features -->
    <div v-if="authStore.isCandidate" class="grid md:grid-cols-3 gap-6 mb-8">
      <button
        @click="activeTab = 'resume'"
        :class="['card text-left', activeTab === 'resume' ? 'border-primary-500 border-2' : '']"
      >
        <div class="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-1">Resume Analysis</h3>
        <p class="text-sm text-gray-600">Get feedback on your resume</p>
      </button>

      <button
        @click="activeTab = 'matching'"
        :class="['card text-left', activeTab === 'matching' ? 'border-primary-500 border-2' : '']"
      >
        <div class="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-1">Job Matching</h3>
        <p class="text-sm text-gray-600">Find jobs that match your skills</p>
      </button>

      <button
        @click="activeTab = 'skills'"
        :class="['card text-left', activeTab === 'skills' ? 'border-primary-500 border-2' : '']"
      >
        <div class="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-1">Skill Recommendations</h3>
        <p class="text-sm text-gray-600">Learn what skills to develop</p>
      </button>
    </div>

    <!-- Recruiter Features -->
    <div v-if="authStore.isRecruiter" class="grid md:grid-cols-3 gap-6 mb-8">
      <button
        @click="activeTab = 'jobDescription'"
        :class="['card text-left', activeTab === 'jobDescription' ? 'border-primary-500 border-2' : '']"
      >
        <div class="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-1">Generate Job Description</h3>
        <p class="text-sm text-gray-600">AI-powered job posting creation</p>
      </button>

      <button
        @click="activeTab = 'screening'"
        :class="['card text-left', activeTab === 'screening' ? 'border-primary-500 border-2' : '']"
      >
        <div class="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-1">Screen Candidates</h3>
        <p class="text-sm text-gray-600">AI-assisted candidate evaluation</p>
      </button>

      <button
        @click="activeTab = 'interviews'"
        :class="['card text-left', activeTab === 'interviews' ? 'border-primary-500 border-2' : '']"
      >
        <div class="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-1">Interview Questions</h3>
        <p class="text-sm text-gray-600">Generate role-specific questions</p>
      </button>
    </div>

    <!-- Candidate: Resume Analysis Tab -->
    <div v-if="authStore.isCandidate && activeTab === 'resume'" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Resume Analysis</h2>
      <p class="text-gray-600 mb-4">Upload your resume or paste the text for AI-powered analysis and feedback</p>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Upload Resume</label>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors">
            <input
              ref="resumeFileInput"
              type="file"
              accept=".pdf,.docx,.txt"
              @change="handleResumeFileUpload"
              class="hidden"
            />
            <button
              type="button"
              @click="$refs.resumeFileInput.click()"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              Choose File
            </button>
            <p class="mt-2 text-sm text-gray-500">PDF, DOCX, or TXT (max 10MB)</p>
            <p v-if="resumeFileName" class="mt-2 text-sm text-primary-600 font-medium">
              Selected: {{ resumeFileName }}
            </p>
          </div>
        </div>
        <div class="text-center text-sm text-gray-500">OR</div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Paste Resume Text</label>
          <textarea
            v-model="resumeText"
            rows="10"
            class="input-field"
            placeholder="Paste your resume text here..."
          ></textarea>
        </div>
      </div>
      <button @click="analyzeResume" :disabled="loading" class="btn-primary mt-4">
        {{ loading ? 'Analyzing...' : 'Analyze Resume' }}
      </button>

      <!-- Resume Analysis Results -->
      <div v-if="result && result.analysis" class="mt-6 space-y-6">
        <!-- ATS Score -->
        <div v-if="result.analysis.ats_score" class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">ATS Compatibility Score</h3>
          <div class="flex items-center space-x-4">
            <div class="relative w-24 h-24">
              <svg class="transform -rotate-90 w-24 h-24">
                <circle cx="48" cy="48" r="40" stroke="#e5e7eb" stroke-width="8" fill="none" />
                <circle cx="48" cy="48" r="40" :stroke="result.analysis.ats_score >= 80 ? '#10b981' : result.analysis.ats_score >= 60 ? '#f59e0b' : '#ef4444'"
                        stroke-width="8" fill="none"
                        :stroke-dasharray="251.2"
                        :stroke-dashoffset="251.2 - (251.2 * result.analysis.ats_score / 100)" />
              </svg>
              <div class="absolute top-0 left-0 w-24 h-24 flex items-center justify-center">
                <span class="text-2xl font-bold">{{ result.analysis.ats_score }}</span>
              </div>
            </div>
            <div class="flex-1">
              <p class="text-gray-700" v-if="result.analysis.ats_explanation">{{ result.analysis.ats_explanation }}</p>
              <p class="text-gray-700" v-else>
                {{ result.analysis.ats_score >= 80 ? 'Excellent! Your resume is highly ATS-compatible.' :
                   result.analysis.ats_score >= 60 ? 'Good, but there\'s room for improvement.' :
                   'Needs improvement to pass ATS systems effectively.' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Extracted Information -->
        <div class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Extracted Information</h3>

          <!-- Skills -->
          <div v-if="result.analysis.key_skills" class="mb-4">
            <h4 class="font-semibold text-gray-800 mb-2">Technical Skills</h4>
            <div class="flex flex-wrap gap-2">
              <span v-for="skill in result.analysis.key_skills.technical_skills" :key="skill"
                    class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                {{ skill }}
              </span>
            </div>

            <h4 class="font-semibold text-gray-800 mb-2 mt-4">Soft Skills</h4>
            <div class="flex flex-wrap gap-2">
              <span v-for="skill in result.analysis.key_skills.soft_skills" :key="skill"
                    class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                {{ skill }}
              </span>
            </div>
          </div>

          <!-- Experience & Education -->
          <div class="grid md:grid-cols-2 gap-4 mt-4">
            <div v-if="result.analysis.years_of_experience">
              <h4 class="font-semibold text-gray-800 mb-2">Experience</h4>
              <p class="text-gray-700">{{ result.analysis.years_of_experience }}</p>
            </div>
            <div v-if="result.analysis.education_background && result.analysis.education_background.length > 0">
              <h4 class="font-semibold text-gray-800 mb-2">Education</h4>
              <div v-for="(edu, idx) in result.analysis.education_background" :key="idx" class="text-gray-700">
                <p class="font-medium">{{ edu.degree }}</p>
                <p class="text-sm">{{ edu.university }} ({{ edu.years }})</p>
                <p class="text-sm" v-if="edu.gpa">GPA: {{ edu.gpa }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Achievements -->
        <div v-if="result.analysis.notable_achievements && result.analysis.notable_achievements.length > 0"
             class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Notable Achievements</h3>
          <ul class="space-y-2">
            <li v-for="(achievement, idx) in result.analysis.notable_achievements" :key="idx"
                class="flex items-start">
              <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span class="text-gray-700">{{ achievement }}</span>
            </li>
          </ul>
        </div>

        <!-- Feedback Sections -->
        <div v-if="result.analysis.formatting_feedback || result.analysis.content_feedback || result.analysis.keyword_suggestions"
             class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Detailed Feedback</h3>

          <!-- Formatting Issues -->
          <div v-if="result.analysis.formatting_feedback && result.analysis.formatting_feedback.length > 0" class="mb-4">
            <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
              <svg class="w-5 h-5 text-orange-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              Formatting Issues
            </h4>
            <ul class="list-disc list-inside space-y-1 ml-7">
              <li v-for="(issue, idx) in result.analysis.formatting_feedback" :key="idx" class="text-gray-700">{{ issue }}</li>
            </ul>
          </div>

          <!-- Content Improvements -->
          <div v-if="result.analysis.content_feedback && result.analysis.content_feedback.length > 0" class="mb-4">
            <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
              <svg class="w-5 h-5 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
              </svg>
              Content Improvements
            </h4>
            <ul class="list-disc list-inside space-y-1 ml-7">
              <li v-for="(feedback, idx) in result.analysis.content_feedback" :key="idx" class="text-gray-700">{{ feedback }}</li>
            </ul>
          </div>

          <!-- Missing Keywords -->
          <div v-if="result.analysis.keyword_suggestions && result.analysis.keyword_suggestions.length > 0" class="mb-4">
            <h4 class="font-semibold text-gray-800 mb-2">Missing Keywords</h4>
            <div class="flex flex-wrap gap-2">
              <span v-for="keyword in result.analysis.keyword_suggestions" :key="keyword"
                    class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
                {{ keyword }}
              </span>
            </div>
          </div>

          <!-- Action Verb Improvements -->
          <div v-if="result.analysis.action_verb_improvements && result.analysis.action_verb_improvements.length > 0">
            <h4 class="font-semibold text-gray-800 mb-2">Strengthen Your Action Verbs</h4>
            <ul class="list-disc list-inside space-y-1 ml-7">
              <li v-for="(verb, idx) in result.analysis.action_verb_improvements" :key="idx" class="text-gray-700">{{ verb }}</li>
            </ul>
          </div>
        </div>

        <!-- Areas for Improvement -->
        <div v-if="result.analysis.areas_for_improvement && result.analysis.areas_for_improvement.length > 0"
             class="bg-yellow-50 rounded-lg border border-yellow-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Key Areas for Improvement</h3>
          <ul class="space-y-3">
            <li v-for="(area, idx) in result.analysis.areas_for_improvement" :key="idx"
                class="flex items-start">
              <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-yellow-500 text-white text-sm font-bold mr-3 flex-shrink-0 mt-0.5">
                {{ idx + 1 }}
              </span>
              <span class="text-gray-700">{{ area }}</span>
            </li>
          </ul>
        </div>

        <!-- Overall Strengths -->
        <div v-if="result.analysis.overall_strengths && result.analysis.overall_strengths.length > 0"
             class="bg-green-50 rounded-lg border border-green-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Your Strengths</h3>
          <ul class="space-y-2">
            <li v-for="(strength, idx) in result.analysis.overall_strengths" :key="idx"
                class="flex items-start">
              <svg class="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span class="text-gray-700 font-medium">{{ strength }}</span>
            </li>
          </ul>
        </div>

        <!-- Summary Recommendation -->
        <div v-if="result.analysis.recommendation_summary"
             class="bg-blue-50 rounded-lg border border-blue-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-3">Summary</h3>
          <p class="text-gray-700 text-lg">{{ result.analysis.recommendation_summary }}</p>
        </div>

        <!-- Debug: Show raw JSON (can be removed later) -->
        <details class="mt-4">
          <summary class="cursor-pointer text-sm text-gray-500 hover:text-gray-700">Show raw data</summary>
          <pre class="mt-2 text-xs text-gray-700 whitespace-pre-wrap bg-gray-100 p-4 rounded">{{ JSON.stringify(result, null, 2) }}</pre>
        </details>
      </div>
    </div>

    <!-- Candidate: Job Matching Tab -->
    <div v-if="authStore.isCandidate && activeTab === 'matching'" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Job Matching</h2>
      <p class="text-gray-600 mb-4">Enter your skills to find matching jobs</p>
      <input
        v-model="skillsInput"
        type="text"
        class="input-field mb-4"
        placeholder="JavaScript, React, HTML, CSS (comma or space-separated)"
      />
      <button @click="findMatchingJobs" :disabled="loading" class="btn-primary">
        {{ loading ? 'Finding matches...' : 'Find Matching Jobs' }}
      </button>

      <!-- Job Matching Results -->
      <div v-if="result && result.recommendations" class="mt-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-bold text-gray-900">Recommended Jobs</h3>
          <span class="text-sm text-gray-600">{{ result.recommendations.length }} matches found</span>
        </div>

        <div v-if="result.recommendations.length === 0" class="text-center py-8 text-gray-500">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <p class="text-lg font-medium">No matching jobs found</p>
          <p class="text-sm">Try different skills or lower your requirements</p>
        </div>

        <div v-else class="space-y-4">
          <div v-for="job in result.recommendations" :key="job.job_id"
               class="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow">
            <!-- Job Header -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h4 class="text-xl font-bold text-gray-900 mb-1">{{ job.title }}</h4>
                <p class="text-gray-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd"/>
                  </svg>
                  {{ job.company }}
                </p>
                <p v-if="job.location" class="text-gray-600 flex items-center mt-1">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                  </svg>
                  {{ job.location }}
                </p>
              </div>

              <!-- Match Score Badge -->
              <div class="ml-4">
                <div class="relative w-20 h-20">
                  <svg class="transform -rotate-90 w-20 h-20">
                    <circle cx="40" cy="40" r="32" stroke="#e5e7eb" stroke-width="6" fill="none" />
                    <circle cx="40" cy="40" r="32"
                            :stroke="job.match_score >= 80 ? '#10b981' : job.match_score >= 60 ? '#f59e0b' : '#3b82f6'"
                            stroke-width="6" fill="none"
                            :stroke-dasharray="201"
                            :stroke-dashoffset="201 - (201 * job.match_score / 100)" />
                  </svg>
                  <div class="absolute top-0 left-0 w-20 h-20 flex items-center justify-center">
                    <span class="text-lg font-bold">{{ Math.round(job.match_score) }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Matching Skills -->
            <div v-if="job.matching_skills && job.matching_skills.length > 0" class="mb-3">
              <h5 class="text-sm font-semibold text-gray-800 mb-2 flex items-center">
                <svg class="w-4 h-4 mr-1 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                You Have
              </h5>
              <div class="flex flex-wrap gap-2">
                <span v-for="skill in job.matching_skills" :key="skill"
                      class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                  {{ skill }}
                </span>
              </div>
            </div>

            <!-- Missing Skills -->
            <div v-if="job.missing_skills && job.missing_skills.length > 0">
              <h5 class="text-sm font-semibold text-gray-800 mb-2 flex items-center">
                <svg class="w-4 h-4 mr-1 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                Skills to Develop
              </h5>
              <div class="flex flex-wrap gap-2">
                <span v-for="skill in job.missing_skills" :key="skill"
                      class="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Candidate: Skills Tab -->
    <div v-if="authStore.isCandidate && activeTab === 'skills'" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Skill Recommendations</h2>
      <p class="text-gray-600 mb-4">Get personalized skill recommendations</p>
      <input
        v-model="currentSkills"
        type="text"
        class="input-field mb-3"
        placeholder="Python Django React (comma or space-separated)"
      />
      <input
        v-model="targetRole"
        type="text"
        class="input-field mb-4"
        placeholder="Target role (e.g., Senior Backend Engineer)..."
      />
      <button @click="getSkillRecommendations" :disabled="loading" class="btn-primary">
        {{ loading ? 'Getting recommendations...' : 'Get Recommendations' }}
      </button>

      <!-- Skill Recommendations Results -->
      <div v-if="result" class="mt-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-900 mb-4">Recommended Skills to Learn</h3>

        <!-- Check if result is an array (list of skills) -->
        <div v-if="Array.isArray(result)" class="space-y-4">
          <div v-for="(skill, idx) in result" :key="idx"
               class="bg-white rounded-lg border-l-4 p-5 shadow-sm hover:shadow-md transition-shadow"
               :class="{
                 'border-red-500': skill.priority === 'High',
                 'border-yellow-500': skill.priority === 'Medium',
                 'border-blue-500': skill.priority === 'Low'
               }">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h4 class="text-lg font-bold text-gray-900">{{ skill.skill }}</h4>
                  <span class="px-3 py-1 rounded-full text-xs font-semibold"
                        :class="{
                          'bg-red-100 text-red-800': skill.priority === 'High',
                          'bg-yellow-100 text-yellow-800': skill.priority === 'Medium',
                          'bg-blue-100 text-blue-800': skill.priority === 'Low'
                        }">
                    {{ skill.priority }} Priority
                  </span>
                </div>

                <p class="text-gray-700 mb-3">{{ skill.reason }}</p>

                <div class="flex items-center text-sm text-gray-600">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                  </svg>
                  <span>Learning Timeline: {{ skill.timeline }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Fallback: Show raw JSON if not an array -->
        <div v-else class="bg-gray-50 rounded-lg p-4">
          <details>
            <summary class="cursor-pointer text-sm text-gray-500 hover:text-gray-700 mb-2">Show raw data</summary>
            <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(result, null, 2) }}</pre>
          </details>
        </div>
      </div>
    </div>

    <!-- Recruiter: Job Description Generator Tab -->
    <div v-if="authStore.isRecruiter && activeTab === 'jobDescription'" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Generate Job Description</h2>
      <p class="text-gray-600 mb-4">Get AI assistance to create compelling job descriptions</p>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
          <input
            v-model="jobDescInput.title"
            type="text"
            class="input-field"
            placeholder="e.g., Senior Full Stack Developer"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
          <input
            v-model="jobDescInput.company"
            type="text"
            class="input-field"
            placeholder="e.g., Tech Corp"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Required Skills</label>
          <input
            v-model="jobDescInput.skills"
            type="text"
            class="input-field"
            placeholder="Python, Django, React, PostgreSQL..."
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Experience Level (years)</label>
          <input
            v-model.number="jobDescInput.experience"
            type="number"
            class="input-field"
            placeholder="5"
          />
        </div>
        <button @click="generateJobDescription" :disabled="loading" class="btn-primary">
          {{ loading ? 'Generating...' : 'Generate Description' }}
        </button>
      </div>

      <div v-if="result" class="mt-6 p-6 bg-white rounded-lg border border-gray-200 shadow-lg">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-bold text-gray-900 text-xl">Generated Job Description</h3>
          <button @click="copyToClipboard(result.job_description)" class="btn-secondary text-sm px-4 py-2">
            📋 Copy to Clipboard
          </button>
        </div>
        <div class="prose prose-blue max-w-none" v-html="formatJobDescription(result.job_description)"></div>
      </div>
    </div>

    <!-- Recruiter: Candidate Screening Tab -->
    <div v-if="authStore.isRecruiter && activeTab === 'screening'" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Screen Candidates</h2>
      <p class="text-gray-600 mb-4">AI-powered candidate evaluation against job requirements</p>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Job Requirements</label>
          <textarea
            v-model="screeningInput.requirements"
            rows="4"
            class="input-field"
            placeholder="Enter the key skills and qualifications needed for this role..."
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Upload Candidate Resume</label>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors">
            <input
              ref="fileInput"
              type="file"
              accept=".pdf,.docx,.txt"
              @change="handleFileUpload"
              class="hidden"
            />
            <button
              type="button"
              @click="$refs.fileInput.click()"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              Choose File
            </button>
            <p class="mt-2 text-sm text-gray-500">PDF, DOCX, or TXT (max 10MB)</p>
            <p v-if="screeningInput.fileName" class="mt-2 text-sm text-primary-600 font-medium">
              Selected: {{ screeningInput.fileName }}
            </p>
          </div>
        </div>
        <div class="text-center text-sm text-gray-500">OR</div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Paste Resume Text</label>
          <textarea
            v-model="screeningInput.resume"
            rows="6"
            class="input-field"
            placeholder="Or paste candidate's resume text here..."
          ></textarea>
        </div>
        <button @click="screenCandidate" :disabled="loading" class="btn-primary">
          {{ loading ? 'Analyzing...' : 'Evaluate Candidate' }}
        </button>
      </div>

      <!-- Screening Results -->
      <div v-if="result && result.analysis" class="mt-6">
        <div class="bg-white rounded-lg border-2 border-primary-200 shadow-xl p-8">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-2xl font-bold text-gray-900 flex items-center">
              <svg class="w-8 h-8 text-primary-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
              </svg>
              Candidate Screening Analysis
            </h3>
            <button @click="copyToClipboard(result.analysis)" class="btn-secondary text-sm px-4 py-2">
              📋 Copy Analysis
            </button>
          </div>

          <div class="screening-analysis prose prose-lg max-w-none" v-html="formatScreeningAnalysis(result.analysis)"></div>
        </div>
      </div>
    </div>

    <!-- Recruiter: Interview Questions Tab -->
    <div v-if="authStore.isRecruiter && activeTab === 'interviews'" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Generate Interview Questions</h2>
      <p class="text-gray-600 mb-4">Create role-specific interview questions tailored to your needs</p>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Job Role</label>
          <input
            v-model="interviewInput.role"
            type="text"
            class="input-field"
            placeholder="e.g., Senior Backend Engineer"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Key Skills to Test</label>
          <input
            v-model="interviewInput.skills"
            type="text"
            class="input-field"
            placeholder="Python, System Design, Database Optimization..."
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Number of Questions</label>
          <input
            v-model.number="interviewInput.count"
            type="number"
            class="input-field"
            placeholder="10"
            min="1"
            max="20"
          />
        </div>
        <button @click="generateInterviewQuestions" :disabled="loading" class="btn-primary">
          {{ loading ? 'Generating...' : 'Generate Questions' }}
        </button>
      </div>

      <div v-if="result" class="mt-6 p-6 bg-white rounded-lg border border-gray-200 shadow-lg">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-gray-900 text-xl">Interview Questions</h3>
          <button @click="copyToClipboard(result.questions)" class="btn-secondary text-sm px-4 py-2">
            📋 Copy to Clipboard
          </button>
        </div>
        <div class="mb-4 p-3 bg-blue-50 rounded-lg">
          <p class="text-sm text-gray-700"><strong>Role:</strong> {{ result.role }}</p>
          <p class="text-sm text-gray-700"><strong>Skills:</strong> {{ result.skills }}</p>
        </div>
        <div class="prose prose-blue max-w-none" v-html="formatJobDescription(result.questions)"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const loading = ref(false)
const result = ref(null)
const fileInput = ref(null)
const resumeFileInput = ref(null)

// Set default active tab based on role
const activeTab = ref(authStore.isRecruiter ? 'jobDescription' : 'resume')

// Candidate inputs
const resumeText = ref('')
const resumeFile = ref(null)
const resumeFileName = ref('')
const skillsInput = ref('')
const currentSkills = ref('')
const targetRole = ref('')

// Recruiter inputs
const jobDescInput = ref({
  title: '',
  company: '',
  skills: '',
  experience: null
})

const screeningInput = ref({
  requirements: '',
  resume: '',
  file: null,
  fileName: ''
})

const interviewInput = ref({
  role: '',
  skills: '',
  count: 10
})

const handleResumeFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size exceeds 10MB. Please choose a smaller file.')
      return
    }
    resumeFile.value = file
    resumeFileName.value = file.name
  }
}

const analyzeResume = async () => {
  loading.value = true
  result.value = null
  try {
    const formData = new FormData()

    if (resumeFile.value) {
      formData.append('resume_file', resumeFile.value)
    } else if (resumeText.value) {
      formData.append('resume_text', resumeText.value)
    } else {
      alert('Please upload a resume file or paste resume text')
      loading.value = false
      return
    }

    const response = await axios.post('/api/ai/candidate/analyze_resume/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    result.value = response.data
  } catch (error) {
    alert('Error analyzing resume: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const findMatchingJobs = async () => {
  loading.value = true
  result.value = null
  try {
    // Support both comma-separated and space-separated skills
    let skills = []
    if (skillsInput.value.includes(',')) {
      // Comma-separated
      skills = skillsInput.value.split(',').map(s => s.trim()).filter(s => s)
    } else {
      // Space-separated
      skills = skillsInput.value.split(/\s+/).map(s => s.trim()).filter(s => s)
    }

    const response = await axios.post('/api/ai/candidate/suggest_jobs/', {
      skills: skills,
      limit: 5
    })
    result.value = response.data
  } catch (error) {
    alert('Error finding jobs: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const getSkillRecommendations = async () => {
  loading.value = true
  result.value = null
  try {
    // Support both comma-separated and space-separated skills
    let skills = []
    if (currentSkills.value.includes(',')) {
      skills = currentSkills.value.split(',').map(s => s.trim()).filter(s => s)
    } else {
      skills = currentSkills.value.split(/\s+/).map(s => s.trim()).filter(s => s)
    }

    const response = await axios.post('/api/ai/candidate/recommend_skills/', {
      current_skills: skills,
      target_role: targetRole.value
    })
    result.value = response.data
  } catch (error) {
    alert('Error getting recommendations: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

// Recruiter Functions
const generateJobDescription = async () => {
  loading.value = true
  result.value = null
  try {
    const response = await axios.post('/api/ai/recruiter/generate_job_description/', {
      position: jobDescInput.value.title,
      company: jobDescInput.value.company,
      requirements: `${jobDescInput.value.experience ? jobDescInput.value.experience + '+ years experience, ' : ''}${jobDescInput.value.skills}`
    })
    result.value = response.data
  } catch (error) {
    alert('Error generating job description: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size exceeds 10MB. Please choose a smaller file.')
      return
    }
    screeningInput.value.file = file
    screeningInput.value.fileName = file.name
  }
}

const screenCandidate = async () => {
  loading.value = true
  result.value = null
  try {
    const formData = new FormData()
    formData.append('job_requirements', screeningInput.value.requirements)

    if (screeningInput.value.file) {
      formData.append('resume_file', screeningInput.value.file)
    } else if (screeningInput.value.resume) {
      formData.append('resume_text', screeningInput.value.resume)
    } else {
      alert('Please upload a resume file or paste resume text')
      loading.value = false
      return
    }

    const response = await axios.post('/api/ai/recruiter/screen_candidate/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    result.value = response.data
  } catch (error) {
    console.error('Screen candidate error:', error.response?.data)
    let errorMsg = 'Error screening candidate: '
    if (error.response?.data) {
      // Handle DRF validation errors
      if (typeof error.response.data === 'object') {
        errorMsg += JSON.stringify(error.response.data, null, 2)
      } else {
        errorMsg += error.response.data.error || error.response.data
      }
    } else {
      errorMsg += error.message
    }
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}

const generateInterviewQuestions = async () => {
  loading.value = true
  result.value = null
  try {
    const response = await axios.post('/api/ai/recruiter/interview_questions/', {
      role: interviewInput.value.role,
      skills: interviewInput.value.skills,
      count: interviewInput.value.count
    })
    result.value = response.data
  } catch (error) {
    alert('Error generating interview questions: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

const formatJobDescription = (text) => {
  if (!text) return ''

  // Split into lines
  let lines = text.split('\n')
  let html = ''
  let inList = false

  lines.forEach(line => {
    line = line.trim()

    if (!line) {
      // Close list if we were in one
      if (inList) {
        html += '</ul>'
        inList = false
      }
      html += '<br>'
      return
    }

    // Check if line is a bullet point
    if (line.startsWith('*') || line.startsWith('-')) {
      if (!inList) {
        html += '<ul class="list-disc ml-6 space-y-2">'
        inList = true
      }
      const content = line.substring(1).trim()
      html += `<li class="text-gray-700">${content}</li>`
    }
    // Check if line is a header (bold text with **...**)
    else if (line.startsWith('**') && line.endsWith('**')) {
      if (inList) {
        html += '</ul>'
        inList = false
      }
      const headerText = line.slice(2, -2)
      html += `<h3 class="section-header">${headerText}</h3>`
    }
    // Regular paragraph
    else {
      if (inList) {
        html += '</ul>'
        inList = false
      }
      // Handle bold text within paragraphs - special styling for headers with colons
      const formatted = line.replace(/\*\*(.*?):\*\*/g, '<span class="inline-header">$1:</span>')
                           .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      html += `<p class="text-gray-700 mb-2">${formatted}</p>`
    }
  })

  // Close list if still open
  if (inList) {
    html += '</ul>'
  }

  return html
}

const formatScreeningAnalysis = (text) => {
  if (!text) return ''

  let html = ''
  const lines = text.split('\n')
  let inList = false

  lines.forEach(line => {
    line = line.trim()

    if (!line) {
      if (inList) {
        html += '</ul>'
        inList = false
      }
      html += '<br>'
      return
    }

    // Check if line is a main header (starts with **)
    if (line.startsWith('**') && line.endsWith('**')) {
      if (inList) {
        html += '</ul>'
        inList = false
      }
      const headerText = line.slice(2, -2).replace(/:/g, '')

      // Color code based on header content
      let colorClass = 'text-blue-600 bg-blue-50 border-blue-300'
      if (headerText.toLowerCase().includes('strength')) {
        colorClass = 'text-green-600 bg-green-50 border-green-300'
      } else if (headerText.toLowerCase().includes('concern') || headerText.toLowerCase().includes('gap')) {
        colorClass = 'text-yellow-600 bg-yellow-50 border-yellow-300'
      } else if (headerText.toLowerCase().includes('recommendation')) {
        colorClass = 'text-purple-600 bg-purple-50 border-purple-300'
      } else if (headerText.toLowerCase().includes('skill')) {
        colorClass = 'text-indigo-600 bg-indigo-50 border-indigo-300'
      }

      html += `<h3 class="text-xl font-bold ${colorClass} px-4 py-3 rounded-lg border-l-4 mb-3 mt-5">${headerText}</h3>`
    }
    // Check if line is a bullet point
    else if (line.startsWith('*') || line.startsWith('-') || line.startsWith('•') || line.startsWith('✅') || line.startsWith('⚠️')) {
      if (!inList) {
        html += '<ul class="list-none ml-2 space-y-2 mb-4">'
        inList = true
      }
      const content = line.substring(1).trim()

      // Add appropriate icon based on content
      let icon = '•'
      let iconColor = 'text-gray-500'
      if (line.startsWith('✅')) {
        icon = '✅'
        iconColor = 'text-green-600'
      } else if (line.startsWith('⚠️')) {
        icon = '⚠️'
        iconColor = 'text-orange-600'
      } else if (content.toLowerCase().includes('strength') || content.toLowerCase().includes('positive')) {
        icon = '✓'
        iconColor = 'text-green-600'
      } else if (content.toLowerCase().includes('concern') || content.toLowerCase().includes('gap')) {
        icon = '⚠'
        iconColor = 'text-yellow-600'
      }

      html += `<li class="flex items-start"><span class="${iconColor} font-bold mr-2">${icon}</span><span class="text-gray-700 flex-1">${content}</span></li>`
    }
    // Regular paragraph
    else {
      if (inList) {
        html += '</ul>'
        inList = false
      }

      // Handle bold text and special formatting
      let formatted = line
        .replace(/\*\*(.*?):\*\*/g, '<strong class="text-gray-900">$1:</strong>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-gray-900">$1</strong>')
        .replace(/(Score:?\s*\d+\/100)/gi, '<span class="px-3 py-1 bg-primary-100 text-primary-800 rounded-full font-bold text-lg">$1</span>')
        .replace(/(Strong Yes|Yes|Maybe|No)/g, function(match) {
          let badgeClass = 'bg-gray-100 text-gray-800'
          if (match === 'Strong Yes') badgeClass = 'bg-green-100 text-green-800'
          else if (match === 'Yes') badgeClass = 'bg-green-100 text-green-700'
          else if (match === 'Maybe') badgeClass = 'bg-yellow-100 text-yellow-800'
          else if (match === 'No') badgeClass = 'bg-red-100 text-red-800'
          return `<span class="px-3 py-1 ${badgeClass} rounded-full font-bold">${match}</span>`
        })

      html += `<p class="text-gray-800 mb-3 leading-relaxed">${formatted}</p>`
    }
  })

  if (inList) {
    html += '</ul>'
  }

  return html
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    alert('Copied to clipboard!')
  }).catch(err => {
    alert('Failed to copy: ' + err.message)
  })
}
</script>


<style scoped>
.prose {
  font-size: 1rem;
  line-height: 1.75;
}

.prose ul {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.prose p {
  margin-bottom: 0.5rem;
}

.prose strong {
  font-weight: 600;
  color: #1f2937;
}

/* Section headers - bold standalone headers */
.prose :deep(.section-header) {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2563eb;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  padding-left: 0.75rem;
  border-left: 4px solid #3b82f6;
  background: linear-gradient(to right, #eff6ff, transparent);
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border-radius: 0.25rem;
}

/* Inline headers - bold text with colons inside paragraphs */
.prose :deep(.inline-header) {
  font-weight: 700;
  color: #1d4ed8;
  font-size: 1.05rem;
  background: linear-gradient(to right, #dbeafe, transparent);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

/* Screening Analysis specific styles */
.screening-analysis {
  font-size: 1.05rem;
  line-height: 1.7;
}

.screening-analysis h3 {
  font-family: system-ui, -apple-system, sans-serif;
  letter-spacing: -0.025em;
}

.screening-analysis ul {
  margin-top: 0.75rem;
  margin-bottom: 1rem;
}

.screening-analysis li {
  padding: 0.5rem 0;
}

.screening-analysis p {
  line-height: 1.8;
}

.screening-analysis strong {
  font-weight: 600;
}
</style>

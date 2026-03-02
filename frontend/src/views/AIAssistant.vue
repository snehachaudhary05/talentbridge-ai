<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- Toast Notification -->
    <transition name="toast">
      <div v-if="toast.show"
           :class="['fixed top-4 right-4 z-50 flex items-center gap-3 px-5 py-4 rounded-xl shadow-2xl text-white text-sm font-medium',
                    toast.type === 'success' ? 'bg-green-600' : 'bg-red-600']">
        <svg v-if="toast.type === 'success'" class="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        <svg v-else class="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        {{ toast.message }}
      </div>
    </transition>

    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">AI Assistant</h1>
      <p class="text-gray-500">
        {{ authStore.isRecruiter ? 'AI-powered tools for smarter recruitment' : 'AI-powered insights for your job search' }}
      </p>
    </div>

    <!-- Candidate Tabs -->
    <div v-if="authStore.isCandidate" class="flex flex-wrap gap-3 mb-6">
      <button v-for="tab in candidateTabs" :key="tab.id"
        @click="switchTab(tab.id)"
        :class="['flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium text-sm transition-all',
                 activeTab === tab.id
                   ? 'bg-primary-600 text-white shadow-md'
                   : 'bg-white text-gray-600 border border-gray-200 hover:border-primary-300 hover:text-primary-600']">
        <span>{{ tab.icon }}</span>
        {{ tab.label }}
      </button>
    </div>

    <!-- Recruiter Tabs -->
    <div v-if="authStore.isRecruiter" class="flex flex-wrap gap-3 mb-6">
      <button v-for="tab in recruiterTabs" :key="tab.id"
        @click="switchTab(tab.id)"
        :class="['flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium text-sm transition-all',
                 activeTab === tab.id
                   ? 'bg-primary-600 text-white shadow-md'
                   : 'bg-white text-gray-600 border border-gray-200 hover:border-primary-300 hover:text-primary-600']">
        <span>{{ tab.icon }}</span>
        {{ tab.label }}
      </button>
    </div>

    <!-- ==============================
         CANDIDATE: RESUME ANALYSIS
         ============================== -->
    <div v-if="authStore.isCandidate && activeTab === 'resume'" class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-1">Resume Analysis</h2>
      <p class="text-gray-500 text-sm mb-5">Upload your resume for AI-powered ATS scoring and feedback</p>

      <div class="space-y-4">
        <div class="border-2 border-dashed border-gray-200 rounded-xl p-6 text-center hover:border-primary-400 transition-colors cursor-pointer bg-gray-50"
             @click="$refs.resumeFileInput.click()">
          <input ref="resumeFileInput" type="file" accept=".pdf,.docx,.txt" @change="handleResumeFileUpload" class="hidden" />
          <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
          </div>
          <p class="text-sm font-medium text-gray-700">Click to upload resume</p>
          <p class="text-xs text-gray-400 mt-1">PDF, DOCX, or TXT · max 10 MB</p>
          <p v-if="resumeFileName" class="mt-2 text-sm text-primary-600 font-semibold">📄 {{ resumeFileName }}</p>
        </div>

        <div class="relative flex items-center">
          <div class="flex-grow border-t border-gray-200"></div>
          <span class="mx-3 text-xs text-gray-400 uppercase tracking-widest">or</span>
          <div class="flex-grow border-t border-gray-200"></div>
        </div>

        <textarea v-model="resumeText" rows="8" class="input-field text-sm" placeholder="Paste your resume text here…"></textarea>
      </div>

      <button @click="analyzeResume" :disabled="loading" class="btn-primary mt-5 flex items-center gap-2">
        <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Analyzing…' : '✨ Analyze Resume' }}
      </button>

      <!-- Resume Results -->
      <div v-if="result && result.analysis" class="mt-8 space-y-6">

        <!-- ATS Score -->
        <div v-if="result.analysis.ats_score" class="bg-gradient-to-br from-gray-50 to-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">ATS Compatibility Score</h3>
          <div class="flex items-center gap-6">
            <div class="relative w-28 h-28 shrink-0">
              <svg class="transform -rotate-90 w-28 h-28">
                <circle cx="56" cy="56" r="46" stroke="#e5e7eb" stroke-width="8" fill="none"/>
                <circle cx="56" cy="56" r="46"
                        :stroke="result.analysis.ats_score >= 80 ? '#10b981' : result.analysis.ats_score >= 60 ? '#f59e0b' : '#ef4444'"
                        stroke-width="8" fill="none"
                        stroke-linecap="round"
                        :stroke-dasharray="289"
                        :stroke-dashoffset="289 - (289 * atsScoreAnimated / 100)"
                        style="transition: stroke-dashoffset 1.2s ease"/>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-3xl font-extrabold leading-none">{{ atsScoreAnimated }}</span>
                <span class="text-xs text-gray-400">/100</span>
              </div>
            </div>
            <div>
              <span :class="['inline-block px-3 py-1 rounded-full text-sm font-semibold mb-2',
                             result.analysis.ats_score >= 80 ? 'bg-green-100 text-green-700' :
                             result.analysis.ats_score >= 60 ? 'bg-yellow-100 text-yellow-700' :
                             'bg-red-100 text-red-700']">
                {{ result.analysis.ats_score >= 80 ? 'Excellent' : result.analysis.ats_score >= 60 ? 'Good' : 'Needs Work' }}
              </span>
              <p class="text-gray-600 text-sm leading-relaxed">
                {{ result.analysis.ats_explanation ||
                   (result.analysis.ats_score >= 80 ? 'Your resume is highly ATS-compatible.' :
                    result.analysis.ats_score >= 60 ? 'Good resume with room for improvement.' :
                    'Needs improvement to pass ATS filters effectively.') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Raw / unstructured response -->
        <div v-if="result.analysis.raw_analysis" class="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Resume Analysis</h3>
          <div class="prose prose-sm max-w-none text-gray-700" v-html="formatMarkdown(result.analysis.raw_analysis)"></div>
        </div>

        <!-- Skills -->
        <div v-if="result.analysis.key_skills" class="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Skills Found</h3>
          <div v-if="result.analysis.key_skills.technical_skills?.length" class="mb-4">
            <p class="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">Technical</p>
            <div class="flex flex-wrap gap-2">
              <span v-for="skill in result.analysis.key_skills.technical_skills" :key="skill"
                    class="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium border border-blue-100">
                {{ skill }}
              </span>
            </div>
          </div>
          <div v-if="result.analysis.key_skills.soft_skills?.length">
            <p class="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">Soft Skills</p>
            <div class="flex flex-wrap gap-2">
              <span v-for="skill in result.analysis.key_skills.soft_skills" :key="skill"
                    class="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium border border-green-100">
                {{ skill }}
              </span>
            </div>
          </div>
        </div>

        <!-- Experience & Education -->
        <div class="grid md:grid-cols-2 gap-4">
          <div v-if="result.analysis.years_of_experience" class="bg-white rounded-2xl border border-gray-200 p-5">
            <p class="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">Experience</p>
            <p class="text-gray-800 font-medium">{{ result.analysis.years_of_experience }}</p>
          </div>
          <div v-if="result.analysis.education_background?.length" class="bg-white rounded-2xl border border-gray-200 p-5">
            <p class="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">Education</p>
            <div v-for="(edu, idx) in result.analysis.education_background" :key="idx" class="mb-2 last:mb-0">
              <p class="font-medium text-gray-800 text-sm">{{ edu.degree }}</p>
              <p class="text-xs text-gray-500">{{ edu.university }} · {{ edu.years }}</p>
              <p v-if="edu.gpa" class="text-xs text-gray-500">GPA: {{ edu.gpa }}</p>
            </div>
          </div>
        </div>

        <!-- Achievements -->
        <div v-if="result.analysis.notable_achievements?.length" class="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Notable Achievements</h3>
          <ul class="space-y-2">
            <li v-for="(a, idx) in result.analysis.notable_achievements" :key="idx" class="flex items-start gap-2">
              <svg class="w-5 h-5 text-green-500 shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span class="text-gray-700 text-sm">{{ a }}</span>
            </li>
          </ul>
        </div>

        <!-- Detailed Feedback -->
        <div v-if="result.analysis.formatting_feedback?.length || result.analysis.content_feedback?.length || result.analysis.keyword_suggestions?.length"
             class="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-5">Detailed Feedback</h3>
          <div class="space-y-5">
            <div v-if="result.analysis.formatting_feedback?.length">
              <p class="text-sm font-semibold text-orange-700 flex items-center gap-1 mb-2">⚠ Formatting Issues</p>
              <ul class="list-disc list-inside space-y-1 ml-2">
                <li v-for="(f, i) in result.analysis.formatting_feedback" :key="i" class="text-sm text-gray-700">{{ f }}</li>
              </ul>
            </div>
            <div v-if="result.analysis.content_feedback?.length">
              <p class="text-sm font-semibold text-blue-700 flex items-center gap-1 mb-2">✏ Content Improvements</p>
              <ul class="list-disc list-inside space-y-1 ml-2">
                <li v-for="(f, i) in result.analysis.content_feedback" :key="i" class="text-sm text-gray-700">{{ f }}</li>
              </ul>
            </div>
            <div v-if="result.analysis.keyword_suggestions?.length">
              <p class="text-sm font-semibold text-purple-700 mb-2">🔑 Missing Keywords</p>
              <div class="flex flex-wrap gap-2">
                <span v-for="kw in result.analysis.keyword_suggestions" :key="kw"
                      class="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-xs font-medium border border-purple-100">
                  {{ kw }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Strengths -->
        <div v-if="result.analysis.overall_strengths?.length"
             class="bg-green-50 rounded-2xl border border-green-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Your Strengths ✅</h3>
          <ul class="space-y-2">
            <li v-for="(s, i) in result.analysis.overall_strengths" :key="i" class="flex items-start gap-2">
              <svg class="w-4 h-4 text-green-600 shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span class="text-sm text-gray-700 font-medium">{{ s }}</span>
            </li>
          </ul>
        </div>

        <!-- Areas for Improvement -->
        <div v-if="result.analysis.areas_for_improvement?.length"
             class="bg-yellow-50 rounded-2xl border border-yellow-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Areas to Improve</h3>
          <ul class="space-y-3">
            <li v-for="(a, i) in result.analysis.areas_for_improvement" :key="i" class="flex items-start gap-3">
              <span class="w-6 h-6 rounded-full bg-yellow-400 text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">{{ i + 1 }}</span>
              <span class="text-sm text-gray-700">{{ a }}</span>
            </li>
          </ul>
        </div>

        <!-- Summary -->
        <div v-if="result.analysis.recommendation_summary"
             class="bg-blue-50 rounded-2xl border border-blue-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-2">Summary</h3>
          <p class="text-gray-700 text-sm leading-relaxed">{{ result.analysis.recommendation_summary }}</p>
        </div>
      </div>
    </div>

    <!-- ==============================
         CANDIDATE: JOB MATCHING
         ============================== -->
    <div v-if="authStore.isCandidate && activeTab === 'matching'" class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-1">Job Matching</h2>
      <p class="text-gray-500 text-sm mb-5">Enter your skills to find the best matching jobs</p>

      <input v-model="skillsInput" type="text" class="input-field mb-4"
             placeholder="JavaScript, React, Node.js (comma or space-separated)" />
      <button @click="findMatchingJobs" :disabled="loading" class="btn-primary flex items-center gap-2">
        <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Searching…' : '🔍 Find Matching Jobs' }}
      </button>

      <div v-if="result && result.recommendations" class="mt-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-900">Recommended Jobs</h3>
          <span class="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">{{ result.recommendations.length }} found</span>
        </div>

        <div v-if="result.recommendations.length === 0" class="text-center py-12 text-gray-400">
          <svg class="w-14 h-14 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <p class="font-medium">No matching jobs found</p>
          <p class="text-sm mt-1">Try different or broader skill terms</p>
        </div>

        <div v-else class="space-y-4">
          <div v-for="job in result.recommendations" :key="job.job_id"
               class="bg-white rounded-2xl border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div class="flex items-start gap-4">
              <div class="flex-1 min-w-0">
                <h4 class="text-base font-bold text-gray-900">{{ job.title }}</h4>
                <p class="text-sm text-gray-500 mt-0.5">{{ job.company }}</p>
                <p v-if="job.location" class="text-xs text-gray-400 mt-0.5">📍 {{ job.location }}</p>
              </div>
              <div class="relative w-16 h-16 shrink-0">
                <svg class="transform -rotate-90 w-16 h-16">
                  <circle cx="32" cy="32" r="26" stroke="#e5e7eb" stroke-width="5" fill="none"/>
                  <circle cx="32" cy="32" r="26"
                          :stroke="job.match_score >= 80 ? '#10b981' : job.match_score >= 60 ? '#f59e0b' : '#3b82f6'"
                          stroke-width="5" fill="none" stroke-linecap="round"
                          :stroke-dasharray="163"
                          :stroke-dashoffset="163 - (163 * job.match_score / 100)"/>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-sm font-bold">{{ Math.round(job.match_score) }}%</span>
                </div>
              </div>
            </div>

            <div class="mt-4 space-y-3">
              <div v-if="job.matching_skills?.length">
                <p class="text-xs font-semibold text-green-700 mb-1.5">✅ You have</p>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="skill in job.matching_skills" :key="skill"
                        class="px-2.5 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium border border-green-100">
                    {{ skill }}
                  </span>
                </div>
              </div>
              <div v-if="job.missing_skills?.length">
                <p class="text-xs font-semibold text-orange-700 mb-1.5">📚 Learn next</p>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="skill in job.missing_skills" :key="skill"
                        class="px-2.5 py-1 bg-orange-50 text-orange-700 rounded-full text-xs font-medium border border-orange-100">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==============================
         CANDIDATE: SKILL RECOMMENDATIONS
         ============================== -->
    <div v-if="authStore.isCandidate && activeTab === 'skills'" class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-1">Skill Recommendations</h2>
      <p class="text-gray-500 text-sm mb-5">Get a personalised roadmap of skills to learn for your target role</p>

      <div class="space-y-3">
        <input v-model="currentSkills" type="text" class="input-field"
               placeholder="Your current skills: Python, Django, React…" />
        <input v-model="targetRole" type="text" class="input-field"
               placeholder="Target role: e.g., Senior Backend Engineer" />
      </div>
      <button @click="getSkillRecommendations" :disabled="loading" class="btn-primary mt-4 flex items-center gap-2">
        <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Getting recommendations…' : '⚡ Get Recommendations' }}
      </button>

      <div v-if="result" class="mt-6 space-y-4">
        <div v-if="Array.isArray(result)">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Your Learning Roadmap</h3>
          <div v-for="(skill, idx) in result" :key="idx"
               :class="['rounded-2xl border-l-4 p-5 bg-white shadow-sm hover:shadow-md transition-shadow',
                        skill.priority === 'High' ? 'border-red-500' :
                        skill.priority === 'Medium' ? 'border-yellow-500' : 'border-blue-500']">
            <div class="flex items-start gap-3">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h4 class="font-bold text-gray-900">{{ skill.skill }}</h4>
                  <span :class="['px-2.5 py-0.5 rounded-full text-xs font-semibold',
                                 skill.priority === 'High' ? 'bg-red-100 text-red-700' :
                                 skill.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                 'bg-blue-100 text-blue-700']">
                    {{ skill.priority }} Priority
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-3">{{ skill.reason }}</p>
                <p class="text-xs text-gray-400 flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                  </svg>
                  {{ skill.timeline }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- Fallback: raw text response -->
        <div v-else-if="result.raw_response || result.note" class="bg-blue-50 rounded-2xl border border-blue-200 p-6">
          <div v-if="result.note" class="text-sm text-blue-700 mb-3 font-medium">{{ result.note }}</div>
          <div v-if="result.raw_response" class="prose prose-sm max-w-none text-gray-700"
               v-html="formatMarkdown(result.raw_response)"></div>
        </div>
      </div>
    </div>

    <!-- ==============================
         RECRUITER: JOB DESCRIPTION
         ============================== -->
    <div v-if="authStore.isRecruiter && activeTab === 'jobDescription'" class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-1">Generate Job Description</h2>
      <p class="text-gray-500 text-sm mb-5">AI-crafted job postings in seconds</p>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="label-sm">Job Title</label>
          <input v-model="jobDescInput.title" type="text" class="input-field" placeholder="e.g., Senior Full Stack Developer"/>
        </div>
        <div>
          <label class="label-sm">Company Name</label>
          <input v-model="jobDescInput.company" type="text" class="input-field" placeholder="e.g., Tech Corp"/>
        </div>
        <div class="md:col-span-2">
          <label class="label-sm">Required Skills</label>
          <input v-model="jobDescInput.skills" type="text" class="input-field" placeholder="Python, Django, React, PostgreSQL…"/>
        </div>
        <div>
          <label class="label-sm">Experience (years)</label>
          <input v-model.number="jobDescInput.experience" type="number" class="input-field" placeholder="5"/>
        </div>
      </div>

      <button @click="generateJobDescription" :disabled="loading" class="btn-primary mt-5 flex items-center gap-2">
        <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Generating…' : '✍️ Generate Description' }}
      </button>

      <div v-if="result" class="mt-6">
        <!-- Header bar -->
        <div class="flex items-center justify-between bg-gradient-to-r from-primary-600 to-primary-700 text-white px-6 py-4 rounded-t-2xl">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center text-lg">📝</div>
            <div>
              <p class="font-bold text-sm">Generated Job Description</p>
              <p class="text-xs text-primary-200">AI-crafted · Ready to post</p>
            </div>
          </div>
          <button @click="copyToClipboard(result.job_description)"
                  class="flex items-center gap-1.5 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-xl text-sm font-medium transition-colors">
            📋 Copy All
          </button>
        </div>
        <!-- Content -->
        <div class="bg-white border border-gray-200 border-t-0 rounded-b-2xl shadow-sm px-8 py-7 job-desc-output">
          <div v-html="formatJobDescription(result.job_description)"></div>
        </div>
      </div>
    </div>

    <!-- ==============================
         RECRUITER: CANDIDATE SCREENING
         ============================== -->
    <div v-if="authStore.isRecruiter && activeTab === 'screening'" class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-1">Screen Candidates</h2>
      <p class="text-gray-500 text-sm mb-5">AI-powered evaluation against your job requirements</p>

      <div class="space-y-4">
        <div>
          <label class="label-sm">Job Requirements</label>
          <textarea v-model="screeningInput.requirements" rows="4" class="input-field"
                    placeholder="List the key skills and qualifications required for this role…"></textarea>
        </div>

        <div class="border-2 border-dashed border-gray-200 rounded-xl p-5 text-center hover:border-primary-400 transition-colors cursor-pointer bg-gray-50"
             @click="$refs.fileInput.click()">
          <input ref="fileInput" type="file" accept=".pdf,.docx,.txt" @change="handleFileUpload" class="hidden"/>
          <p class="text-sm font-medium text-gray-700">Click to upload candidate resume</p>
          <p class="text-xs text-gray-400 mt-1">PDF, DOCX, or TXT · max 10 MB</p>
          <p v-if="screeningInput.fileName" class="mt-2 text-sm text-primary-600 font-semibold">📄 {{ screeningInput.fileName }}</p>
        </div>

        <div class="relative flex items-center">
          <div class="flex-grow border-t border-gray-200"></div>
          <span class="mx-3 text-xs text-gray-400 uppercase tracking-widest">or paste text</span>
          <div class="flex-grow border-t border-gray-200"></div>
        </div>

        <textarea v-model="screeningInput.resume" rows="5" class="input-field"
                  placeholder="Paste candidate's resume text here…"></textarea>

        <button @click="screenCandidate" :disabled="loading" class="btn-primary flex items-center gap-2">
          <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ loading ? 'Evaluating…' : '🔎 Evaluate Candidate' }}
        </button>
      </div>

      <div v-if="result && result.analysis" class="mt-6 rounded-2xl overflow-hidden shadow-lg border border-gray-200">

        <!-- Report header -->
        <div class="bg-gradient-to-r from-slate-800 to-slate-700 text-white px-6 py-5">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center text-2xl shrink-0">🧑‍💼</div>
              <div>
                <p class="font-bold text-base">Candidate Evaluation Report</p>
                <p class="text-slate-300 text-xs mt-0.5">AI-powered screening · Gemini Flash</p>
              </div>
            </div>

            <div class="flex items-center gap-4">
              <!-- Score circle -->
              <div v-if="screeningScore > 0" class="relative w-16 h-16 shrink-0">
                <svg class="transform -rotate-90 w-16 h-16">
                  <circle cx="32" cy="32" r="26" stroke="rgba(255,255,255,0.15)" stroke-width="5" fill="none"/>
                  <circle cx="32" cy="32" r="26"
                          :stroke="screeningScore >= 80 ? '#10b981' : screeningScore >= 60 ? '#f59e0b' : '#ef4444'"
                          stroke-width="5" fill="none" stroke-linecap="round"
                          :stroke-dasharray="163"
                          :stroke-dashoffset="163 - (163 * screeningScoreAnimated / 100)"
                          style="transition: stroke-dashoffset 1.2s ease"/>
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <span class="text-base font-extrabold leading-none">{{ screeningScoreAnimated }}</span>
                  <span class="text-xs text-slate-400 leading-none">/100</span>
                </div>
              </div>

              <!-- Recommendation badge -->
              <div v-if="screeningRecommendation">
                <span :class="['px-4 py-2 rounded-xl font-bold text-sm whitespace-nowrap',
                               screeningRecommendation === 'Strong Yes' ? 'bg-green-500 text-white' :
                               screeningRecommendation === 'Yes' ? 'bg-green-400 text-white' :
                               screeningRecommendation === 'Maybe' ? 'bg-yellow-500 text-white' :
                               'bg-red-500 text-white']">
                  {{ screeningRecommendation === 'Strong Yes' ? '🌟 Strong Yes' :
                     screeningRecommendation === 'Yes' ? '✅ Yes' :
                     screeningRecommendation === 'Maybe' ? '🤔 Maybe' : '❌ No' }}
                </span>
              </div>

              <button @click="copyToClipboard(result.analysis)"
                      class="flex items-center gap-1.5 px-3 py-2 bg-white/15 hover:bg-white/25 rounded-xl text-xs font-medium transition-colors shrink-0">
                📋 Copy
              </button>
            </div>
          </div>
        </div>

        <!-- Report body -->
        <div class="bg-gray-50 px-6 py-6">
          <div class="screening-analysis space-y-4" v-html="formatScreeningAnalysis(result.analysis)"></div>
        </div>
      </div>
    </div>

    <!-- ==============================
         RECRUITER: INTERVIEW QUESTIONS
         ============================== -->
    <div v-if="authStore.isRecruiter && activeTab === 'interviews'" class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-1">Generate Interview Questions</h2>
      <p class="text-gray-500 text-sm mb-5">Role-specific questions tailored to your needs</p>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="label-sm">Job Role</label>
          <input v-model="interviewInput.role" type="text" class="input-field" placeholder="e.g., Senior Backend Engineer"/>
        </div>
        <div>
          <label class="label-sm">Number of Questions</label>
          <input v-model.number="interviewInput.count" type="number" class="input-field" min="1" max="20" placeholder="10"/>
        </div>
        <div class="md:col-span-2">
          <label class="label-sm">Key Skills to Test</label>
          <input v-model="interviewInput.skills" type="text" class="input-field" placeholder="Python, System Design, Database Optimization…"/>
        </div>
      </div>

      <button @click="generateInterviewQuestions" :disabled="loading" class="btn-primary mt-5 flex items-center gap-2">
        <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Generating…' : '❓ Generate Questions' }}
      </button>

      <div v-if="result" class="mt-6 bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-gray-900 text-lg">Interview Questions</h3>
          <button @click="copyToClipboard(result.questions)" class="btn-secondary text-sm px-4 py-2 flex items-center gap-1.5">
            📋 Copy
          </button>
        </div>
        <div class="flex gap-3 mb-4 p-3 bg-gray-50 rounded-xl text-sm text-gray-600">
          <span><strong>Role:</strong> {{ result.role }}</span>
          <span class="text-gray-300">|</span>
          <span><strong>Skills:</strong> {{ result.skills }}</span>
        </div>
        <div class="prose prose-sm max-w-none" v-html="formatJobDescription(result.questions)"></div>
      </div>
    </div>

    <!-- ==============================
         AI CHAT (shared for both roles)
         ============================== -->
    <div v-if="activeTab === 'chat'" class="flex flex-col bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden"
         style="height: 70vh;">

      <!-- Chat header -->
      <div class="flex items-center gap-3 px-5 py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white">
        <div class="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center text-lg">🤖</div>
        <div>
          <p class="font-semibold text-sm">TalentBridge AI</p>
          <p class="text-xs text-primary-200">
            {{ authStore.isRecruiter ? 'Ask me about candidates, hiring, job postings…' : 'Ask me about jobs, your resume, career growth…' }}
          </p>
        </div>
      </div>

      <!-- Messages -->
      <div ref="chatContainer" class="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-gray-50">
        <!-- Welcome message -->
        <div v-if="chatMessages.length === 0" class="flex flex-col items-center justify-center h-full text-center py-8">
          <div class="text-5xl mb-4">💬</div>
          <p class="text-gray-600 font-medium mb-2">How can I help you today?</p>
          <p class="text-gray-400 text-sm mb-6">Ask anything about your {{ authStore.isRecruiter ? 'hiring process' : 'job search' }}</p>
          <div class="flex flex-wrap gap-2 justify-center max-w-lg">
            <button v-for="suggestion in chatSuggestions" :key="suggestion"
                    @click="sendSuggestion(suggestion)"
                    class="px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm text-gray-600 hover:border-primary-400 hover:text-primary-600 transition-colors">
              {{ suggestion }}
            </button>
          </div>
        </div>

        <!-- Message bubbles -->
        <div v-for="(msg, idx) in chatMessages" :key="idx"
             :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
          <div v-if="msg.role === 'assistant'" class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-sm shrink-0 mr-2 mt-1">🤖</div>
          <div :class="['max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
                        msg.role === 'user'
                          ? 'bg-primary-600 text-white rounded-br-sm'
                          : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm']">
            <div v-if="msg.role === 'assistant'" v-html="formatMarkdown(msg.content)"></div>
            <span v-else>{{ msg.content }}</span>
          </div>
          <div v-if="msg.role === 'user'" class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-xs font-bold shrink-0 ml-2 mt-1">
            {{ userInitial }}
          </div>
        </div>

        <!-- Typing indicator -->
        <div v-if="chatLoading" class="flex justify-start">
          <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-sm shrink-0 mr-2 mt-1">🤖</div>
          <div class="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
            <div class="flex gap-1 items-center h-4">
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="px-4 py-3 border-t border-gray-200 bg-white">
        <div class="flex gap-2 items-end">
          <textarea v-model="chatInput" @keydown.enter.exact.prevent="sendChatMessage"
                    rows="1" class="flex-1 resize-none rounded-xl border border-gray-200 px-4 py-2.5 text-sm focus:outline-none focus:border-primary-400 focus:ring-2 focus:ring-primary-100"
                    placeholder="Type a message… (Enter to send)"
                    style="max-height: 120px; overflow-y: auto"></textarea>
          <button @click="sendChatMessage" :disabled="chatLoading || !chatInput.trim()"
                  class="w-10 h-10 rounded-xl bg-primary-600 hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-white transition-colors shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
          </button>
        </div>
        <p class="text-xs text-gray-400 mt-1.5 ml-1">Enter to send · Shift+Enter for new line</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const loading = ref(false)
const result = ref(null)
const fileInput = ref(null)
const resumeFileInput = ref(null)
const chatContainer = ref(null)

// ATS score animation
const atsScoreAnimated = ref(0)

// Toast
const toast = ref({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 3500)
}

// Tabs
const candidateTabs = [
  { id: 'resume', label: 'Resume Analysis', icon: '📄' },
  { id: 'matching', label: 'Job Matching', icon: '🎯' },
  { id: 'skills', label: 'Skill Recommendations', icon: '⚡' },
  { id: 'chat', label: 'AI Chat', icon: '💬' }
]
const recruiterTabs = [
  { id: 'jobDescription', label: 'Job Description', icon: '✍️' },
  { id: 'screening', label: 'Screen Candidates', icon: '🔎' },
  { id: 'interviews', label: 'Interview Questions', icon: '❓' },
  { id: 'chat', label: 'AI Chat', icon: '💬' }
]

const activeTab = ref(authStore.isRecruiter ? 'jobDescription' : 'resume')

const switchTab = (tabId) => {
  activeTab.value = tabId
  result.value = null
}

// Watch ATS score to animate it
watch(() => result.value?.analysis?.ats_score, (score) => {
  if (!score) return
  atsScoreAnimated.value = 0
  const target = score
  const step = target / 40
  const interval = setInterval(() => {
    atsScoreAnimated.value = Math.min(Math.round(atsScoreAnimated.value + step), target)
    if (atsScoreAnimated.value >= target) clearInterval(interval)
  }, 30)
})

// Screening score + recommendation (extracted from AI text)
const screeningScore = ref(0)
const screeningScoreAnimated = ref(0)
const screeningRecommendation = ref('')

watch(() => result.value?.analysis, (analysis) => {
  if (!analysis) { screeningScore.value = 0; screeningRecommendation.value = ''; return }
  // Extract score: "Score: 92/100"
  const scoreMatch = analysis.match(/Score:?\s*(\d+)\s*\/\s*100/i)
  if (scoreMatch) {
    const target = parseInt(scoreMatch[1])
    screeningScore.value = target
    screeningScoreAnimated.value = 0
    const step = target / 40
    const interval = setInterval(() => {
      screeningScoreAnimated.value = Math.min(Math.round(screeningScoreAnimated.value + step), target)
      if (screeningScoreAnimated.value >= target) clearInterval(interval)
    }, 30)
  }
  // Extract recommendation
  const recMatch = analysis.match(/Recommendation:?\s*\[?\s*(Strong\s+Yes|Yes|Maybe|No)\s*\]?/i)
  if (recMatch) screeningRecommendation.value = recMatch[1].replace(/\s+/g, ' ').trim()
})

// ── Candidate inputs ──
const resumeText = ref('')
const resumeFile = ref(null)
const resumeFileName = ref('')
const skillsInput = ref('')
const currentSkills = ref('')
const targetRole = ref('')

// ── Recruiter inputs ──
const jobDescInput = ref({ title: '', company: '', skills: '', experience: null })
const screeningInput = ref({ requirements: '', resume: '', file: null, fileName: '' })
const interviewInput = ref({ role: '', skills: '', count: 10 })

// ── Chat ──
const chatMessages = ref([])
const chatInput = ref('')
const chatLoading = ref(false)
const conversationId = ref(null)

const userInitial = computed(() => {
  const name = authStore.user?.first_name || authStore.user?.email || 'U'
  return name[0].toUpperCase()
})

const chatSuggestions = computed(() => {
  if (authStore.isRecruiter) return [
    'How do I write a compelling job description?',
    'What interview questions reveal culture fit?',
    'How do I evaluate a candidate quickly?',
    'What red flags should I look for in resumes?'
  ]
  return [
    'How can I improve my ATS score?',
    'What skills are in demand for software engineers?',
    'How do I negotiate a higher salary?',
    'Tips for a strong cover letter?'
  ]
})

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// ── File uploads ──
const handleResumeFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  if (file.size > 10 * 1024 * 1024) { showToast('File exceeds 10 MB limit', 'error'); return }
  resumeFile.value = file
  resumeFileName.value = file.name
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  if (file.size > 10 * 1024 * 1024) { showToast('File exceeds 10 MB limit', 'error'); return }
  screeningInput.value.file = file
  screeningInput.value.fileName = file.name
}

// ── Candidate actions ──
const analyzeResume = async () => {
  if (!resumeFile.value && !resumeText.value) {
    showToast('Please upload a file or paste resume text', 'error'); return
  }
  loading.value = true; result.value = null
  try {
    const formData = new FormData()
    if (resumeFile.value) formData.append('resume_file', resumeFile.value)
    else formData.append('resume_text', resumeText.value)
    const response = await axios.post('/ai/candidate/analyze_resume/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    result.value = response.data
  } catch (error) {
    showToast('Analysis failed: ' + (error.response?.data?.error || error.message), 'error')
  } finally { loading.value = false }
}

const findMatchingJobs = async () => {
  if (!skillsInput.value.trim()) { showToast('Please enter your skills', 'error'); return }
  loading.value = true; result.value = null
  try {
    const skills = skillsInput.value.includes(',')
      ? skillsInput.value.split(',').map(s => s.trim()).filter(Boolean)
      : skillsInput.value.split(/\s+/).map(s => s.trim()).filter(Boolean)
    const response = await axios.post('/ai/candidate/suggest_jobs/', { skills, limit: 5 })
    result.value = response.data
  } catch (error) {
    showToast('Failed to find jobs: ' + (error.response?.data?.error || error.message), 'error')
  } finally { loading.value = false }
}

const getSkillRecommendations = async () => {
  if (!currentSkills.value.trim() || !targetRole.value.trim()) {
    showToast('Please fill in both fields', 'error'); return
  }
  loading.value = true; result.value = null
  try {
    const skills = currentSkills.value.includes(',')
      ? currentSkills.value.split(',').map(s => s.trim()).filter(Boolean)
      : currentSkills.value.split(/\s+/).map(s => s.trim()).filter(Boolean)
    const response = await axios.post('/ai/candidate/recommend_skills/', {
      current_skills: skills, target_role: targetRole.value
    })
    result.value = response.data
  } catch (error) {
    showToast('Failed to get recommendations: ' + (error.response?.data?.error || error.message), 'error')
  } finally { loading.value = false }
}

// ── Recruiter actions ──
const generateJobDescription = async () => {
  if (!jobDescInput.value.title || !jobDescInput.value.company) {
    showToast('Please enter job title and company', 'error'); return
  }
  loading.value = true; result.value = null
  try {
    const response = await axios.post('/ai/recruiter/generate_job_description/', {
      position: jobDescInput.value.title,
      company: jobDescInput.value.company,
      requirements: `${jobDescInput.value.experience ? jobDescInput.value.experience + '+ years experience, ' : ''}${jobDescInput.value.skills}`
    })
    result.value = response.data
  } catch (error) {
    showToast('Generation failed: ' + (error.response?.data?.error || error.message), 'error')
  } finally { loading.value = false }
}

const screenCandidate = async () => {
  if (!screeningInput.value.requirements) { showToast('Please enter job requirements', 'error'); return }
  if (!screeningInput.value.file && !screeningInput.value.resume) {
    showToast('Please upload a resume or paste text', 'error'); return
  }
  loading.value = true; result.value = null
  try {
    const formData = new FormData()
    formData.append('job_requirements', screeningInput.value.requirements)
    if (screeningInput.value.file) formData.append('resume_file', screeningInput.value.file)
    else formData.append('resume_text', screeningInput.value.resume)
    const response = await axios.post('/ai/recruiter/screen_candidate/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    result.value = response.data
  } catch (error) {
    showToast('Screening failed: ' + (error.response?.data?.error || error.message), 'error')
  } finally { loading.value = false }
}

const generateInterviewQuestions = async () => {
  if (!interviewInput.value.role || !interviewInput.value.skills) {
    showToast('Please fill in role and skills', 'error'); return
  }
  loading.value = true; result.value = null
  try {
    const response = await axios.post('/ai/recruiter/interview_questions/', {
      role: interviewInput.value.role,
      skills: interviewInput.value.skills,
      count: interviewInput.value.count
    })
    result.value = response.data
  } catch (error) {
    showToast('Generation failed: ' + (error.response?.data?.error || error.message), 'error')
  } finally { loading.value = false }
}

// ── Chat ──
const sendSuggestion = (text) => {
  chatInput.value = text
  sendChatMessage()
}

const sendChatMessage = async () => {
  const message = chatInput.value.trim()
  if (!message || chatLoading.value) return

  chatMessages.value.push({ role: 'user', content: message })
  chatInput.value = ''
  chatLoading.value = true
  await scrollChatToBottom()

  try {
    // Create conversation on first message
    if (!conversationId.value) {
      const conv = await axios.post('/ai/conversations/', { title: 'Chat' })
      conversationId.value = conv.data.id
    }

    const response = await axios.post(`/ai/conversations/${conversationId.value}/send_message/`, { message })
    chatMessages.value.push({ role: 'assistant', content: response.data.message })
  } catch (error) {
    chatMessages.value.push({
      role: 'assistant',
      content: '⚠️ Sorry, I couldn\'t process that. Please try again.'
    })
  } finally {
    chatLoading.value = false
    await scrollChatToBottom()
  }
}

// ── Helpers ──
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => showToast('Copied to clipboard!'))
    .catch(() => showToast('Copy failed — please copy manually', 'error'))
}

const formatMarkdown = (text) => {
  if (!text) return ''
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^### (.*?)$/gm, '<h4 class="text-base font-bold text-gray-900 mt-4 mb-1">$1</h4>')
    .replace(/^## (.*?)$/gm, '<h3 class="text-lg font-bold text-gray-900 mt-5 mb-2">$1</h3>')
    .replace(/^# (.*?)$/gm, '<h2 class="text-xl font-bold text-gray-900 mt-5 mb-2">$1</h2>')
    .replace(/^[-*] (.*?)$/gm, '<li class="ml-4 text-gray-700 text-sm">$1</li>')
    .replace(/(<li.*<\/li>\n?)+/g, (match) => `<ul class="list-disc list-inside space-y-1 mb-3">${match}</ul>`)
    .replace(/\n\n/g, '</p><p class="mb-3">')
    .replace(/\n/g, '<br>')
}

// Inline bold/italic helper
const boldInline = (text) =>
  text
    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900 font-semibold">$1</strong>')
    .replace(/(?<!\*)\*(?!\*)([^*]+)(?<!\*)\*(?!\*)/g, '<em>$1</em>')

const formatJobDescription = (text) => {
  if (!text) return ''
  const lines = text.split('\n')
  let html = ''
  let inBulletList = false
  let inNumberedList = false
  let optionCount = 0

  const closeLists = () => {
    if (inBulletList) { html += '</ul>'; inBulletList = false }
    if (inNumberedList) { html += '</ol>'; inNumberedList = false }
  }

  lines.forEach(raw => {
    const line = raw.trim()

    // Blank line
    if (!line) { closeLists(); return }

    // Horizontal rule  (-- or --- or ────)
    if (/^[-─]{2,}$/.test(line)) {
      closeLists()
      html += '<div class="my-6 border-t border-dashed border-gray-200"></div>'
      return
    }

    // Numbered list  "1. text"
    const numMatch = line.match(/^(\d+)\.\s+(.+)/)
    if (numMatch) {
      if (inBulletList) { html += '</ul>'; inBulletList = false }
      if (!inNumberedList) {
        html += '<ol class="space-y-2 mb-4 ml-1">'
        inNumberedList = true
      }
      html += `<li class="flex items-start gap-3">
        <span class="w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">${numMatch[1]}</span>
        <span class="text-gray-700 text-sm leading-relaxed">${boldInline(numMatch[2])}</span>
      </li>`
      return
    }

    // Section header patterns produced by AI:
    //   **Header text**       (standard)
    //   *Header text**        (single start, double end)
    //   **Header text:**      (with trailing colon)
    //   *Header text:*        (single star both sides)
    // Detect: line is ALL bold (no other non-star content outside the stars)
    const headerMatch = line.match(/^\*{1,2}([^*]{2,}?)\*{0,2}:?\s*$/)
    if (headerMatch) {
      const inner = headerMatch[1].replace(/:+$/, '').trim()
      // Skip if inner text is suspiciously short or is just punctuation
      if (inner.length > 2) {
        closeLists()
        // "Option N" headers get a chip-style badge
        if (/^option\s*\d/i.test(inner)) {
          optionCount++
          html += `<div class="mt-8 mb-3 flex items-center gap-3">
            <span class="px-3 py-1 bg-primary-600 text-white rounded-full text-xs font-bold uppercase tracking-wide">
              ${inner}
            </span>
            <div class="flex-1 border-t border-gray-200"></div>
          </div>`
        } else {
          // Normal section header
          html += `<h3 class="text-sm font-bold text-gray-900 uppercase tracking-wide mt-5 mb-2 flex items-center gap-2">
            <span class="w-1 h-4 bg-primary-500 rounded-full inline-block"></span>
            ${inner}
          </h3>`
        }
        return
      }
    }

    // Bullet  "- text"  "* text"  "• text"
    // (must NOT be a header-style line already caught above)
    if (/^[-*•]\s+/.test(line)) {
      if (inNumberedList) { html += '</ol>'; inNumberedList = false }
      if (!inBulletList) {
        html += '<ul class="space-y-2 mb-4 ml-1">'
        inBulletList = true
      }
      const content = line.replace(/^[-*•]\s+/, '')
      html += `<li class="flex items-start gap-2.5">
        <span class="mt-2 w-1.5 h-1.5 rounded-full bg-primary-400 shrink-0"></span>
        <span class="text-gray-700 text-sm leading-relaxed">${boldInline(content)}</span>
      </li>`
      return
    }

    // Regular paragraph
    closeLists()

    // Lines that look like "Key Considerations & Customization:" (plain text pseudo-headers)
    if (/^[A-Z][^.!?]{5,40}[:\?]$/.test(line)) {
      html += `<p class="text-sm font-semibold text-gray-800 mt-4 mb-1">${boldInline(line)}</p>`
      return
    }

    html += `<p class="text-gray-700 text-sm leading-relaxed mb-2">${boldInline(line)}</p>`
  })

  closeLists()
  return html
}

const formatScreeningAnalysis = (text) => {
  if (!text) return ''

  // Section styling by keyword
  const getSectionCfg = (title) => {
    const t = title.toLowerCase()
    if (t.includes('overall') || t.includes('assessment')) return { icon: '🎯', border: 'border-blue-400',   bg: 'bg-blue-50',   head: 'text-blue-800'   }
    if (t.includes('strength'))                              return { icon: '💪', border: 'border-green-400',  bg: 'bg-green-50',  head: 'text-green-800'  }
    if (t.includes('experience') || t.includes('achieve'))  return { icon: '🏆', border: 'border-violet-400', bg: 'bg-violet-50', head: 'text-violet-800' }
    if (t.includes('skill'))                                 return { icon: '🛠️', border: 'border-indigo-400', bg: 'bg-indigo-50', head: 'text-indigo-800' }
    if (t.includes('concern') || t.includes('gap'))         return { icon: '⚠️', border: 'border-yellow-400', bg: 'bg-yellow-50', head: 'text-yellow-800' }
    if (t.includes('cultural') || t.includes('soft'))       return { icon: '🤝', border: 'border-teal-400',   bg: 'bg-teal-50',   head: 'text-teal-800'   }
    if (t.includes('recommendation'))                        return { icon: '✅', border: 'border-emerald-400',bg: 'bg-emerald-50',head: 'text-emerald-800'}
    if (t.includes('next') || t.includes('step'))           return { icon: '📋', border: 'border-slate-400',  bg: 'bg-slate-50',  head: 'text-slate-700'  }
    return                                                          { icon: '📌', border: 'border-primary-300',bg: 'bg-primary-50',head: 'text-primary-800'}
  }

  // Split into sections using --- dividers
  const sections = text.split(/\n---+\n?/)
  let html = ''

  sections.forEach(section => {
    const lines = section.trim().split('\n')
    if (!lines.length) return

    // Find the section title: ### **Title** or ## Title or **Title**
    let titleLine = ''
    let contentLines = []
    let foundTitle = false

    for (let i = 0; i < lines.length; i++) {
      const l = lines[i].trim()
      if (!foundTitle) {
        // Skip the top-level ## title (report title)
        if (/^##\s+[^#]/.test(l)) { foundTitle = true; continue }
        // ### **Title** or ### Title
        const h3Match = l.match(/^###\s+\*{0,2}(.*?)\*{0,2}:?\s*$/)
        if (h3Match) { titleLine = h3Match[1].replace(/\*{1,2}/g, '').replace(/:$/,'').trim(); foundTitle = true; continue }
        // **Title** alone on a line
        const boldMatch = l.match(/^\*{1,2}([^*]{3,}?)\*{1,2}:?\s*$/)
        if (boldMatch) { titleLine = boldMatch[1].replace(/:$/,'').trim(); foundTitle = true; continue }
      }
      contentLines.push(lines[i])
    }

    if (!titleLine && !contentLines.filter(l => l.trim()).length) return

    const cfg = titleLine ? getSectionCfg(titleLine) : null

    if (cfg && titleLine) {
      html += `<div class="rounded-xl border-l-4 ${cfg.border} ${cfg.bg} overflow-hidden mb-1">`
      html += `<div class="flex items-center gap-2 px-4 py-3 border-b border-white/60">
        <span class="text-base">${cfg.icon}</span>
        <h3 class="font-bold text-sm uppercase tracking-wide ${cfg.head}">${titleLine}</h3>
      </div>`
      html += `<div class="px-4 py-3">${renderSectionContent(contentLines)}</div>`
      html += '</div>'
    } else {
      // No title (intro paragraph or report title block)
      const inner = renderSectionContent(contentLines)
      if (inner.trim()) {
        html += `<div class="bg-white rounded-xl border border-gray-200 px-4 py-3 mb-1">${inner}</div>`
      }
    }
  })

  return html
}

// Render the content lines within a section
const renderSectionContent = (lines) => {
  let html = ''
  let inBullet = false
  let inNumbered = false
  let subSection = ''

  const closeLists = () => {
    if (inBullet) { html += '</ul>'; inBullet = false }
    if (inNumbered) { html += '</ol>'; inNumbered = false }
  }

  lines.forEach(raw => {
    const line = raw.trim()
    if (!line) { closeLists(); return }

    // Sub-section headers: #### ✅ ... or #### ⚠️ ...
    const subH = line.match(/^####\s+(.+)/)
    if (subH) {
      closeLists()
      const stxt = subH[1].trim()
      let subCls = 'text-gray-700 bg-white/60 border-gray-200'
      if (stxt.includes('✅') || stxt.toLowerCase().includes('met') || stxt.toLowerCase().includes('required')) subCls = 'text-green-700 bg-green-50 border-green-200'
      else if (stxt.includes('⚠️') || stxt.toLowerCase().includes('gap') || stxt.toLowerCase().includes('missing')) subCls = 'text-yellow-700 bg-yellow-50 border-yellow-200'
      html += `<p class="text-xs font-bold uppercase tracking-wide ${subCls} border rounded-lg px-3 py-1.5 mb-2 mt-3 inline-flex items-center gap-1">${stxt}</p><br>`
      return
    }

    // Numbered list
    const numMatch = line.match(/^(\d+)\.\s+(.+)/)
    if (numMatch) {
      if (inBullet) { html += '</ul>'; inBullet = false }
      if (!inNumbered) { html += '<ol class="space-y-2 mt-2 mb-1">'; inNumbered = true }
      html += `<li class="flex items-start gap-2.5">
        <span class="w-5 h-5 rounded-full bg-white border border-current text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 opacity-70">${numMatch[1]}</span>
        <span class="text-sm leading-relaxed">${boldInline(numMatch[2])}</span>
      </li>`
      return
    }

    // Bullet: *, -, •  (leading spaces ok)
    if (/^\s*[-*•]\s+/.test(raw)) {
      if (inNumbered) { html += '</ol>'; inNumbered = false }
      if (!inBullet) { html += '<ul class="space-y-2 mt-2 mb-1">'; inBullet = true }
      const content = line.replace(/^[-*•]\s+/, '')
      html += `<li class="flex items-start gap-2">
        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-current opacity-50 shrink-0"></span>
        <span class="text-sm leading-relaxed">${boldInline(content)}</span>
      </li>`
      return
    }

    // Regular paragraph
    closeLists()
    let fmt = boldInline(line)
      .replace(/(Score:?\s*\d+\/100)/gi, '<span class="px-2 py-0.5 bg-white/80 border border-current/30 rounded-full font-bold text-sm">$1</span>')
      .replace(/\[?(Strong\s+Yes|Yes|Maybe|No)\]?(?=\s|$)/g, (m, rec) => {
        const r = rec.trim()
        const cls = r === 'Strong Yes' ? 'bg-green-500' : r === 'Yes' ? 'bg-green-400' : r === 'Maybe' ? 'bg-yellow-500' : 'bg-red-500'
        return `<span class="inline-block px-3 py-0.5 ${cls} text-white rounded-full font-bold text-sm">${r}</span>`
      })
    html += `<p class="text-sm leading-relaxed mb-1.5">${fmt}</p>`
  })

  closeLists()
  return html
}
</script>


<style scoped>
.label-sm {
  @apply block text-sm font-medium text-gray-700 mb-1.5;
}

/* Toast animation */
.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(1rem); }
.toast-leave-to   { opacity: 0; transform: translateX(1rem); }

/* Screening analysis */
.screening-analysis { font-size: 0.9rem; line-height: 1.7; }
.screening-analysis ul, .screening-analysis ol { list-style: none; margin: 0; padding: 0; }
.screening-analysis li + li { margin-top: 0.4rem; }

/* Job description output */
.job-desc-output { font-family: inherit; }
.job-desc-output h3 { letter-spacing: 0.05em; }
.job-desc-output ul, .job-desc-output ol { margin: 0; padding: 0; list-style: none; }
</style>

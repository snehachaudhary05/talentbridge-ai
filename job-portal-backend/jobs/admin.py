from django.contrib import admin
from .models import Job, Application, SavedJob, Interview


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'job_type', 'status', 'recruiter', 'created_at']
    list_filter = ['status', 'job_type', 'is_remote', 'created_at']
    search_fields = ['title', 'company_name', 'description', 'required_skills']
    readonly_fields = ['created_at', 'updated_at', 'views_count']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company_name', 'description')
        }),
        ('Job Details', {
            'fields': ('job_type', 'location', 'is_remote', 'salary_min', 'salary_max')
        }),
        ('Requirements', {
            'fields': ('requirements', 'responsibilities', 'required_skills')
        }),
        ('Management', {
            'fields': ('recruiter', 'status', 'deadline')
        }),
        ('Metadata', {
            'fields': ('views_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'status', 'skill_match_score', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['candidate__email', 'job__title', 'resume_text']
    readonly_fields = ['applied_at', 'updated_at', 'skill_match_score', 'ai_summary']

    fieldsets = (
        ('Application Info', {
            'fields': ('job', 'candidate', 'status')
        }),
        ('Submitted Data', {
            'fields': ('cover_letter', 'resume_text', 'resume_file_url')
        }),
        ('AI Analysis', {
            'fields': ('skill_match_score', 'ai_summary')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at')
        }),
    )


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'job__title']
    readonly_fields = ['created_at']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'scheduled_datetime', 'interview_type', 'status', 'created_at']
    list_filter = ['status', 'interview_type', 'scheduled_datetime', 'created_at']
    search_fields = ['application__candidate__email', 'application__job__title', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'scheduled_datetime'

    fieldsets = (
        ('Interview Details', {
            'fields': ('application', 'scheduled_datetime', 'duration_minutes', 'interview_type')
        }),
        ('Location/Meeting', {
            'fields': ('location', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'reminder_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

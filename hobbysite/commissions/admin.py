"""Admin config for Commission and Comment"""

from django.contrib import admin
from .models import Commission, Job, JobApplication


class JobInLine(admin.TabularInline):
    """Inline admin for jobs"""
    model = Job


class CommissionAdmin(admin.ModelAdmin):
    """Admin for Commission"""
    model = Commission
    inlines = [JobInLine]


class JobAdmin(admin.ModelAdmin):
    """Admin for Job model"""
    model = Job


class JobApplicationAdmin(admin.ModelAdmin):
    """Admin for the JobApplcation model"""
    model = JobApplication


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)

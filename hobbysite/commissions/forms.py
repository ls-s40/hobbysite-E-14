"""Forms for the commissions, jobs, and job applications"""

from django import forms
from .models import Commission, Job, JobApplication

class CommissionForm(forms.ModelForm):
    """
    Form for Commissions
    """
    class Meta:
        """
        Metaclass for implementing the Commission Form
        """
        model = Commission
        fields = ['title', 'description', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class JobForm(forms.ModelForm):
    """
    Form for Jobs
    """
    class Meta:
        """
        Metaclass for implementing the Job Form
        """
        model = Job
        fields = ['role', 'manpower_required', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class JobApplicationForm(forms.ModelForm):
    """
    Form for Job Applications
    """
    class Meta:
        """
        Metaclass for implementing the Job Application Form
        """
        model = JobApplication
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

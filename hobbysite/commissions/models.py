"""Models for commissions and comments"""

from django.db import models
from django.urls import reverse
from user_management.models import Profile

class Commission(models.Model):
    """Commission model"""
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued')
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metaclass for how the commissions are ordered
        """
        ordering = ['created_on']

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        """Returns the absolute URL for a commission"""
        return reverse('commissions:commissions_detail', args=[str(self.id)])

    def update_status(self):
        """Updates the status of the commission instance"""
        jobs = self.job_set.all()
        total_accepted = 0
        total_manpower = 0

        for job in jobs:
            total_accepted += job.jobapplication_set.filter(status='Accepted').count()
            total_manpower += job.manpower_required

        if total_accepted >= total_manpower:
            self.status = 'Full'
            self.save()


class Job(models.Model):
    """Comment model"""
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full')
    ]

    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    class Meta:
        """
        Metaclass for how the jobs are ordered
        """
        ordering = [
            models.Case(
                models.When(status='Open', then=0),
                models.When(status='Full', then=1),
                output_field=models.IntegerField()
            ),
            '-manpower_required',
            'role'
        ]

    def __str__(self):
        return f"{self.role} for {self.commission.title}"

    def update_status(self):
        """Updates the status of the job instance"""
        accepted = self.jobapplication_set.filter(status='Accepted').count()
        if accepted >= self.manpower_required and self.status != 'Full':
            self.status = 'Full'
            self.save()

    def count_job_slots(self):
        """Returns how many available slots are left for the job instance"""
        return self.manpower_required - self.jobapplication_set.filter(status='Accepted').count()


class JobApplication(models.Model):
    """Represents a user's application to a job."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.user.username} applied to {self.job.role}"

    class Meta:
        """
        Metaclass for how the job applications are ordered
        """
        ordering = [
            models.Case(
                models.When(status='Pending', then=0),
                models.When(status='Accepted', then=1),
                models.When(status='Rejected', then=2),
                output_field=models.IntegerField()
            ),
            '-applied_on'
        ]

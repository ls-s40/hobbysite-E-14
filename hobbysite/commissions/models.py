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
        ordering = ['created_on']
    
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        """Returns the absolute URL for a commission"""
        return reverse('commissions:commissions_detail', args=[str(self.id)])

    """
    def update_status(self):
        jobs = self.job_set
    """


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

    # BAKA MALI
    class Meta:
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
        ordering = [
            models.Case(
                models.When(status='Pending', then=0),
                models.When(status='Accepted', then=1),
                models.When(status='Rejected', then=2),
                output_field=models.IntegerField()
            ),
            '-applied_on'
        ]

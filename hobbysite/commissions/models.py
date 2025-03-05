from django.db import models
from django.urls import reverse

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commissions_detail', args=[str(self.id)])
    

class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  
    updated_on = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'Comment on {self.commission.title} at {self.created_on}'




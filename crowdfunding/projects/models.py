from django.contrib.auth import get_user_model
from django.db import models  

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_start = models.DateTimeField(null=True)
    date_ending = models.DateTimeField(null=True)
    #category = models.CharField(max_length=200)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        default='Uncategorised'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200) 
 
class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
        )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
        )

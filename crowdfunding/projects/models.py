from django.contrib.auth import get_user_model
from django.db import models  

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modefied_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Project(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_start = models.DateTimeField()
    date_ending = models.DateTimeField()
    #category = models.CharField(max_length=200)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        default='Uncategorised',
        related_name='category_projects'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )

    def save(self, **kwargs):
        super().save(**kwargs)
        # then check for badges
        self.owner.badge_check('owner_projects')

class Category(BaseModel):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)

 
class Pledge(BaseModel):
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

    def save(self, **kwargs):
        super().save(**kwargs)
        # then check for badges
        self.supporter.badge_check('supporter_pledges')

class Comment(BaseModel):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name="comments"
        )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="author_comments")
    body = models.TextField()
    visible = models.BooleanField(default=True)

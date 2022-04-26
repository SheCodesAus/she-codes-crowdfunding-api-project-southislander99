from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_image = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    social = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.username

    def badge_check(self, badge_type:str):
        """ check to see if user needs badges """
        count = getattr(self, badge_type).count()
        existing_badge_ids = list(self.badges.filter(badge_type=badge_type).values_list('id', flat=True))
        for badge in Badge.objects.filter(badge_type=badge_type):
            if badge.badge_goal <= count:
                if badge.id not in existing_badge_ids:
                    self.badges.add(badge)

BADGE_TYPES = (
    ('owner_projects', 'Project'),
    ('supporter_pledges', 'Pledge'),
)

# 1. Projects Badges // 2. Pledge Badges
class Badge(models.Model):
    image = models.URLField()
    users = models.ManyToManyField("users.CustomUser", related_name="badges")
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    badge_goal = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            ('badge_type', 'badge_goal'),
        )

    def __str__(self) -> str:
        return f"{self.badge_type}:{self.badge_goal}"


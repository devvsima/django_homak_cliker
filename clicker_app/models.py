# clicker_app/models.py
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    upgrade_level = models.PositiveIntegerField(default=1)
    bot_level = models.PositiveIntegerField(default=0)
    last_bot_collect = models.DateTimeField(default=timezone.now)
    character = models.CharField(max_length=50, default='hamster')
    character_bonus = models.PositiveIntegerField(default=1)  # Новый бонус персонажа

    def __str__(self):
        return f"{self.user.username} - {self.score} - Upgrade Level: {self.upgrade_level} - Bot Level: {self.bot_level} - Character: {self.character}"

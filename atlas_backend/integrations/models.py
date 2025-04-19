# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleCalendarIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_token = models.CharField(max_length=512)
    calendar_id = models.CharField(max_length=255)

class MicrosoftCalendarIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    microsoft_token = models.CharField(max_length=512)
    calendar_id = models.CharField(max_length=255)

class SlackIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_token = models.CharField(max_length=512)

class TrelloIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trello_token = models.CharField(max_length=512)
    board_id = models.CharField(max_length=255)

class AsanaIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asana_token = models.CharField(max_length=512)
    workspace_id = models.CharField(max_length=255)

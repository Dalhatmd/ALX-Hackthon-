from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='led_teams'
    )
    members = models.ManyToManyField(
        User,
        related_name='teams'
    )
    def __str__(self):
        return self.name

class TeamInvitation(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_team_invitations"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_team_invitations"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="invitations"
    )
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team", "recipient")

    

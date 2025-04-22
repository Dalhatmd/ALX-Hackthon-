from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Team, TeamInvitation
from .serializers import TeamSerializer, TeamInvitationSerializer, UserSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import models

User = get_user_model()

class TeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show teams where user is either leader or member
        return Team.objects.filter(
            models.Q(leader=self.request.user) | 
            models.Q(members=self.request.user)
        ).distinct()

class TeamDetailView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to teams the user is part of
        return Team.objects.filter(
            models.Q(leader=self.request.user) | 
            models.Q(members=self.request.user)
        ).distinct()

class TeamMembersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        try:
            team = Team.objects.get(id=team_id)
            # Verify the requesting user is part of the team
            if self.request.user == team.leader or self.request.user in team.members.all():
                return team.members.all()
            raise PermissionDenied("You are not a member of this team")
        except Team.DoesNotExist:
            raise ValidationError("Team does not exist")

class RemoveTeamMemberView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, team_id, user_id):
        try:
            team = Team.objects.get(id=team_id)
            user_to_remove = User.objects.get(id=user_id)
            
            # Only team leader can remove members
            if request.user != team.leader:
                raise PermissionDenied("Only team leader can remove members")
            
            # Can't remove the leader
            if user_to_remove == team.leader:
                raise ValidationError("Cannot remove team leader")
            
            # Remove the user if they're a member
            if user_to_remove in team.members.all():
                team.members.remove(user_to_remove)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError("User is not a member of this team")
            
        except Team.DoesNotExist:
            raise ValidationError("Team does not exist")
        except User.DoesNotExist:
            raise ValidationError("User does not exist")

class TeamInvitationCreateView(generics.CreateAPIView):
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        try:
            team = Team.objects.get(id=team_id)
            
            # Only team leader can send invitations
            if self.request.user != team.leader:
                raise PermissionDenied("Only team leader can send invitations")
            
            recipient_email = serializer.validated_data['recipient_email']
            
            try:
                recipient = User.objects.get(email=recipient_email)
            except User.DoesNotExist:
                raise ValidationError("User with this email does not exist")
            
            # Check if user is already in the team
            if recipient == team.leader or recipient in team.members.all():
                raise ValidationError("User is already in the team")
            
            # Check if invitation already exists
            if TeamInvitation.objects.filter(team=team, recipient=recipient).exists():
                raise ValidationError("Invitation already sent to this user")
            
            serializer.save(sender=self.request.user, recipient=recipient, team=team)
            
        except Team.DoesNotExist:
            raise ValidationError("Team does not exist")

class TeamInvitationListView(generics.ListAPIView):
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show invitations sent by or received by the current user
        return TeamInvitation.objects.filter(
            models.Q(sender=self.request.user) | 
            models.Q(recipient=self.request.user)
        )

from django.urls import path
from .views import (
    TeamListView,
    TeamDetailView,
    TeamMembersView,
    RemoveTeamMemberView,
    TeamInvitationCreateView,
    TeamInvitationListView,
)

urlpatterns = [
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('teams/<int:team_id>/members/', TeamMembersView.as_view(), name='team-members'),
    path('teams/<int:team_id>/members/<int:user_id>/', RemoveTeamMemberView.as_view(), name='remove-team-member'),
    path('teams/<int:team_id>/invite/', TeamInvitationCreateView.as_view(), name='team-invite'),
    path('invitations/', TeamInvitationListView.as_view(), name='invitation-list'),
]

from django.urls import path
from .views import SignupView, LoginView, status_view, UserInfoView, MeView, UpdateUserView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('status', status_view, name='status'),
    path('info/<int:pk>/', UserInfoView.as_view, name="user-info"),
    path('me/', MeView.as_view(), name="user-me"),
    path('update/', UpdateUserView.as_view(), name='update-user')
]

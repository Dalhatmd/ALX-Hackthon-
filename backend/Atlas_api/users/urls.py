from django.urls import path
from .views import SignupView, LoginView, status_view

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('status', status_view, name='status')
]

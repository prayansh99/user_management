from django.urls import path
from .views import SignupView, LoginView, LogoutView, UserDetailView, UserDetailByUsernameView

urlpatterns = [
    path('register_user', SignupView.as_view(), name='register_user'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user_profile/<str:user_id>', UserDetailView.as_view(), name='user_profile'),
    path('user_profile/username/<str:username>', UserDetailByUsernameView.as_view(), name='user_profile_by_username'),
]

from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('posts/', views.posts,name='posts'),
    path('posts/<int:id>',views.posts,name='posts'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/',views.signup,name='register'),
    path('user/login/',views.login,name='login'),
    path('user/profile/',views.user_profile,name='profile'),
    path('user/change-password/',views.change_password,name='change_password'),
    path('user/send-password-reset-email/',views.send_password_reset_email,
         name="send_password_reset_email"),
    path('user/reset-password/<uid>/<token>/',views.password_reset_view,
         name='password_reset_view')
]
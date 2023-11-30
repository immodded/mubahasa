from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("password_update/", views.PasswordUpdateView.as_view(),name="password_update"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("profile_update/",views.ProfileUpdateView.as_view(),name="profile_update"),
    path("profile_list/",views.ProfileListView.as_view(),name="profile_list"),
    path('profile/<int:pk>/update/', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('profile/<int:pk>/',views.UserProfileDetailView.as_view(),name="user_profile_detail"),


]

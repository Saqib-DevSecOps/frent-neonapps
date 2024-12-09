from django.urls import path, include

from src.services.users.views import UserListView, UserDetailView, UserUpdateView, UserPasswordResetView, SocialsView, \
    remove_social_account

app_name = "users"
urlpatterns = [

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),
    path('socials/', SocialsView.as_view(), name='social-accounts'),
    path('remove-social-auth/<int:account_id>/', remove_social_account, name='remove_social_account'),

]
urlpatterns += [
    path('user/api/', include('src.services.users.api.urls', namespace='users-api')),
]

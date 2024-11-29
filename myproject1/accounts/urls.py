from django.urls import path
from .views import RegisterView, LoginView, DashboardView
from .views import CreateUserView, UserDetailView, UpdateUserView, DeleteUserView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),  # Fetch user details
    path('user/<int:user_id>/update/', UpdateUserView.as_view(), name='update_user'),  # Update user
    path('user/<int:user_id>/delete/', DeleteUserView.as_view(), name='delete_user'),  # Delete user
]





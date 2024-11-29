# accounts/authentication.py

# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model

# class EmailBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None):
#         User = get_user_model()  # This will fetch the custom user model
#         try:
#             user = User.objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None

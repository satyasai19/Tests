# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Generate a username if it's not provided. Default to email's local part
        username = validated_data.get('username', validated_data['email'].split('@')[0])  

        # Ensure username uniqueness if you're allowing email-based usernames
        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": "This username is already taken."})

        # Create the user using the create_user method which hashes the password
        user = User.objects.create_user(
            username=username,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']  # automatically hashed by create_user
        )
        return user


User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Validate email field
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ValidationError("Email and password are required.")

        # Check if the user with the provided email exists
        user = User.objects.filter(email=email).first()
        
        if not user:
            raise ValidationError("Email address not found.")
        
        # Check if the password is correct
        if not user.check_password(password):
            raise ValidationError("Incorrect password.")
        
        # Generate JWT token (or any other type of token) upon successful validation
        refresh = RefreshToken.for_user(user)
        
        # Return the token data in the response
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    # Define the serializer to handle CRUD operations for the default User model
    class Meta:
        model = User  # Using the default User model
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Overriding the create method to hash the password before saving
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        # Overriding the update method to handle user updates
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        # Only update password if it's provided
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance

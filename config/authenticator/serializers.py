from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
# Serializers for User Registration 
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all(),
                                         message="User with this email already exists.")])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

# validate email uniqueness and password confirmation
    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

# validate password confirmation
    def validate(self, attrs):
        password  = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password!= confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
# create user and set is_active and is_verified to False
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active = False,
            is_verified = False
        )
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
# Serializer for User Login
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    
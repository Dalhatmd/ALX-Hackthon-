from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['email', 'password', 'user_type']
        extra_kwargs = {
            'user_type': {'required': True}
        }
    
    def validate(self, attrs):
        # Validate user_type is one of the allowed choices
        valid_user_types = [User.UserType.ADMIN, User.UserType.GENERAL, 
                           User.UserType.EMPLOYEE, User.UserType.OWNER, User.UserType.TEAM_LEADER]
        if attrs['user_type'] not in valid_user_types:
            raise serializers.ValidationError({"user_type": "Invalid user type selected."})
            
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone", "user_type", "team_leader", "date_joined")


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'phone', 'password']

    def validate(self, attrs):
        if 'user_type' in self.initial_data:
            raise serializers.ValidationError("You cannot change user type")
        return attrs

    def update(self, instance, validated_data):
        # Update password if provided
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)  # hash the new password
        instance.save()
        return instance


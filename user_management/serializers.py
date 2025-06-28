from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import re

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        
        if len(data['password']) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', data['password']):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', data['password']):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', data['password']):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', data['password']):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return data
    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username doesn't exist.")
        
        user = authenticate(username = data['username'], password = data['password'])

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        data['user'] = user

        return data
    
    def get_jwt_token(self, validated_data):
        user = validated_data['user']
        refresh =  RefreshToken.for_user(user)

        return {"message": "Login Success", "data": {"token": {"refresh":str(refresh),"access":str(refresh.access_token)}}}

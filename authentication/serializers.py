from rest_framework import serializers
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from . models import CustomUser
from django.db.models import Q 
class LoginSerializer(serializers.Serializer):

    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username_or_email = data.get('username_or_email')
        password =  data.get('password')

        if username_or_email and password:
            # Check if the input is an email address
            if '@' in username_or_email:
                # If email address, try to fetch user by email
                user = CustomUser.objects.filter(email=username_or_email).first()
            else:
                # Otherwise, try to fetch user by username
                user = CustomUser.objects.filter(username=username_or_email).first()
            
            if user:
                # If user exists, attempt to authenticate
                user = authenticate(username=user.username, password=password)
                if user:
                    data['user'] = user
                    return data
            raise serializers.ValidationError("Invalid username/email or password.")
        else:
            raise serializers.ValidationError("Must include 'username_or_email' and 'password' fields.")
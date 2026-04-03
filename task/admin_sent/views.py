from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import random
import string
from .models import User
# Create your views here.


class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        
        if user is None:
            return Response({"error": "invalid credentials"}, status=400)
        
        if not user.is_admin:
            return Response({"error": "only admin can login"}, status=403)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
        


class CreateUserView(APIView):

    def post(self, request):
        if not request.user.is_admin:
            return Response({"error": "Only admin can create users"}, status=403)

        email = request.data.get("email")
        username = request.data.get("username")

        # Generate random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        # Send email
        send_mail(
            subject="Your Login Credentials",
            message=f"Username: {username}\nPassword: {password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "User created and email sent"})
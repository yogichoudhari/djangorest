from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from home.models import (Post,User)
from .serializers import (PostsSerializer,UserSerializer,UserLoginSerializer,
                          UserProfileSerializer,ChangePasswordSerializer,
                          SendPasswordResetEmailSerializer,ResetPasswordSerializer)
from rest_framework_simplejwt.tokens import RefreshToken

#token generation view 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }
    
#posts get request view

@api_view(['GET','POST'])
@parser_classes([MultiPartParser, FormParser,FileUploadParser])
@permission_classes([IsAuthenticated])
def posts(request,id=None):
    if request.method=='GET':
        print(request.user.username)
        if id is not None:
            post = Post.objects.get(pk=id)
            serialize = PostsSerializer(post,context={'request':request})
            return Response(serialize.data)
        posts = Post.objects.all()
        serialize = PostsSerializer(posts,many=True,context={'request':request})
        return Response(serialize.data,status=status.HTTP_200_OK)

#signup view 
@api_view(['POST'])
def signup(request):
    serialize = UserSerializer(data=request.data)
    if serialize.is_valid():
        user = serialize.save()
        token = get_tokens_for_user(user)
        return Response({'response':"user created",'token':token},status=status.HTTP_201_CREATED)
    return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

#login view
@api_view(['POST'])
def login(request):
    serialize = UserLoginSerializer(data=request.data)
    if serialize.is_valid():
        email = serialize.data.get('email')
        password = serialize.data.get('password')
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            token = get_tokens_for_user(user)
            return Response({'message':'login Sucessfully','token':token},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['email or password is incorrect']}},
                        status=status.HTTP_404_NOT_FOUND)
    return Response({'errors':serialize.errors},status=status.HTTP_400_BAD_REQUEST)

#user profile view
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser,FormParser])
def user_profile(request):
    serialize = UserProfileSerializer(request.user)
    return Response(serialize.data,status=status.HTTP_200_OK)

#changepassword view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serialize = ChangePasswordSerializer(data=request.data,context={'user':request.user})
    if serialize.is_valid():
        return Response({'status':'Password Changed Successfully'},status=status.HTTP_200_OK)
    return Response({'erros':serialize.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_password_reset_email(request):
    serialize = SendPasswordResetEmailSerializer(data=request.data)
    if serialize.is_valid():
        return Response({"msg":"Reset Password Email has been sent to you successfully"},
                        status=status.HTTP_200_OK)
    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password_reset_view(request,uid,token):
    serializer = ResetPasswordSerializer(data=request.data,
                                         context={'uid':uid,'token':token})
    if serializer.is_valid():
        return Response({'msg':'password reset done'},status=status.HTTP_200_OK)
    return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

                                        
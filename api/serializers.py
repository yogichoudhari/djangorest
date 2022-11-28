from rest_framework import serializers
from home.models import Post,User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
# class AuthUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AuthUser
#         fields = ['username','email','first_name','last_name']
#     def create(self,validated_data):
#         return AuthUser.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField("get_image_url")
    class Meta:
        model = User
        fields =['id','username','email','bio','password','profile_pic']
    def get_image_url(self,obj):
        request = self.context.get('request')
        photo_url = obj.profile_pic.url
        return request.build_absolute_uri(photo_url)
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields=['id','username','email','bio','profile_pic']

class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=80,min_length=8)
    password2 = serializers.CharField(max_length=80,min_length=8) 
    
    def validate(self,attrs):
        password1 =attrs.get('password1')
        password2 =attrs.get('password2')
        user = self.context.get('user')
        if password1!=password2:
            raise serializers.ValidationError('password did not match')  
        user.set_password(password1)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']
        
    def validate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            url = f'http://127.0.0.1:8000/api/user/reset-password/{uid}/{token}'
            def send_password_reset_link(url,email):
                subject = 'Password Reset Link'
                from_email = settings.EMAIL_HOST_USER
                recipient_list=[email]
                message = f'''Hie there\n
                this is an official email for your password reset\n
                Please click on the link to reset the password\n
                {url}'''
                send_mail(subject, message, from_email, recipient_list)
            send_password_reset_link(url,email)
            return attrs
        else:
            raise serialzers.ValidationError("Incorrect Email User doesnt exists")

class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=80,min_length=8)
    password2 = serializers.CharField(max_length=80,min_length=8)
    def validate(self,attrs):
        pass1 = attrs.get('password1')
        pass2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if pass1!=pass2:
            raise serializers.ValidationError('password did not match')
        user_id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serialzers.ValidationError('token is not valid')
        user.set_password(pass1)
        return attrs
            
class PostsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Post
        fields = ['id','user','image_url','discription','likes']
    def get_image_url(self,obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)
       
    def create(self,validated_data):
        return Posts.objects.create(**validated_data)
    
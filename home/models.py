from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email=None, username=None, profile_pic=None,bio=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            bio=bio,
            profile_pic=profile_pic
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='media')
    bio = models.TextField(max_length=300,blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


#this mode is of no use now i have created custom user model

# class Handler(models.Model):
#     user = models.OneToOneField(auth_user, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500)
#     image = models.ImageField(upload_to='media')
#     token = models.CharField(max_length=100)
#     is_varified = models.BooleanField(default=False)
    

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    discription = models.CharField(max_length=300)
    likes = models.PositiveIntegerField(default=0)
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
    

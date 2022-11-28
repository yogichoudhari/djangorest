from django.contrib import admin
from .models import (User,Post,Comment)
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import (UserCreationForm,UserChangeForm)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'username','bio','profile_pic', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','bio','profile_pic')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','profile_pic','bio', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','user','image','discription','likes']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','comments']
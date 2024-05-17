from django.contrib import admin
from .models import UserProfile,MuaGoi
# Register your models here.

admin.site.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mota', 'vitri', 'birth_date', 'nickname', 'avatar', 'account_name']
    
    
admin.site.register(MuaGoi)
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mota = models.TextField(max_length=500, blank=True, default='')
    vitri = models.CharField(max_length=50, blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    nickname = models.CharField(max_length=50, blank=True, default='')
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    account_name = models.CharField(max_length=30, blank=True, default='') 
    additional_info = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'user_profile' 
        
    def __str__(self):
        return self.account_name or self.nickname 
    

        
        


class MuaGoi(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    tengoi = models.CharField(max_length=100)
    giagoi = models.DecimalField(max_digits=10, decimal_places=2)
    thoihan = models.CharField(max_length=100)
    phuongthucthanhtoan = models.CharField(max_length=100)
    ngaymuagoi = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.user_profile} - {self.tengoi}'
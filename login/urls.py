from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name="register"), 
    path('logout/', views.logout_User, name='logout'),
    path('profile/', views.profile , name='profile'),
    path('thongbao/', views.thongbao, name='thongbao'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('muagoi/', views.muagoi, name='muagoi'),
    path('thanhtoan/', views.thanhtoan, name='thanhtoan'),
    path('process_thanhtoan/', views.process_thanhtoan, name='process_thanhtoan'),
    path('user_mua_goi/',views.user_mua_goi, name='user_mua_goi')
]

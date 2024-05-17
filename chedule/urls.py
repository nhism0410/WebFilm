from django.urls import path
from . import views

app_name = 'chedule'

urlpatterns = [
    path('', views.dangchieu, name='dangchieu'),
    path('sapchieu/', views.sapchieu, name='sapchieu'),
    path('hoanthanh/', views.hoanthanh, name='hoanthanh'),
    path('lichchieu/', views.lichchieu , name='lichchieu'),
    path('dangxem/', views.high_rated_films_view, name='high_rated_films'),
    path('top-10-most-viewed-films/', views.top_10_most_viewed_films, name='top_10_most_viewed_films'),
    path('followed_films/', views.followed_films, name='followed_films'),
    path('confirm_unfollow/<int:film_id>/', views.confirm_unfollow, name='confirm_unfollow'),
    path('unfollow/<int:film_id>/', views.unfollow, name='unfollow'),
    path('history/', views.history, name='history'),
]

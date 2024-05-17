from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('info_films/<int:id>', views.info_films, name='info_films'),
    path('movie/<int:id>', views.movie, name='movie'),
    path('post_comment/<int:film_id>', views.post_comment, name='post_comment'),
    path('rate/<int:film_id>/', views.rate_film, name='rate_film'),
    path('toggle_follow/<int:film_id>/', views.toggle_follow, name='toggle_follow'),
    path('search/', views.search, name='search'),
    path('post_comment_movie/<int:tap_film_id>', views.post_comment_movie, name='post_comment_movie'),
]
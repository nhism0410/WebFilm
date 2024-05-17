from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('<int:id>', views.category, name='category'),
    path('film_one_chap/', views.film_one_chap, name='film_one_chap')
]

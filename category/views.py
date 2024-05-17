from django.shortcuts import render
from .models import Category
from home.models import Film
from django.shortcuts import get_object_or_404

# Create your views here.

def category(request, id):
    category_films = Film.objects.filter(theloai=id)
    category_title = get_object_or_404(Category, id=id).title   
    return render(request, 'category/category.html', {"category_films": category_films, "category_title": category_title})



def film_one_chap(request):
    category_films = Film.objects.filter(theloai__title__icontains="Phim chiếu rạp") 
    return render(request, 'category/film_one_chap.html', {"category_films": category_films})



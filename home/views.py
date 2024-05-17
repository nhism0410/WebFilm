from django.shortcuts import render,redirect,get_object_or_404
from .models import  Film,Comment, RateFilm
from chedule.models import TapFilm
from django.core.paginator import Paginator
from chedule.views import schedule, get_high_rated_films
from django.contrib import messages
from .forms import CommentForm,ReplyForm
from login.models import UserProfile
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg 
# Create your views here.

    
def home(request):
    all_films = Film.objects.all()
    paginator = Paginator(all_films, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    chedule = schedule()
    return render(request,'home/home.html', {"films" : page_obj,'chedule': chedule})



def info_films(request, id):
    film_cm = Film.objects.prefetch_related('comment_set').get(pk=id)
    total_comments = film_cm.comment_set.count()
    comments = film_cm.comment_set.order_by('-id') 
    total_tapfilm = film_cm.total_episodes
    get_year = film_cm.get_year()
    latest_episode = film_cm.latest_episode()
    all_episodes = film_cm.all_episodes()
    
    # Phân trang cho danh sách bình luận
    paginator = Paginator(comments, 6)  # Chia danh sách bình luận thành các trang, mỗi trang có tối đa 10 bình luận
    page_number = request.GET.get('page')  # Lấy số trang từ query string
    page_obj = paginator.get_page(page_number)  # Lấy đối tượng trang hiện tại

    # Tính điểm vote trung bình
    ratings = RateFilm.objects.filter(film=film_cm)
    total_votes = ratings.count()
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'home/info_films.html', {
        'film_cm': film_cm, 
        "latest_episode": latest_episode,
        "total_tapfilm": total_tapfilm, 
        "get_year": get_year,
        "all_episodes": all_episodes,
        'total_comments': total_comments,
        'comments': comments,
        'total_votes': total_votes,
        'average_rating': average_rating,
        'comments': page_obj,
    })


def increment_view_count(film_id):
    film = TapFilm.objects.get(pk=film_id)
    film.view_count += 1
    film.save()

def post_comment(request, film_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            film = Film.objects.get(pk=film_id)
            comment_content = form.cleaned_data['comment']
            user_profile = None
            user = request.user
            if user.is_authenticated:
                if hasattr(user, 'userprofile'):
                    user_profile = user.userprofile
                elif user.email:
                    user_profile = UserProfile.objects.create(user=user, account_name=user.username, email=user.email)
            current_time = timezone.now()
            new_comment = Comment.objects.create(film_cm=film, user_profile=user_profile, comment=comment_content, created_at=current_time)
            messages.success(request, 'Bình luận của bạn đã được gửi.')
            return redirect('home:info_films', id=film_id)
        else:
            print(form.errors)  # In ra lỗi để debug
    else:
        current_time = timezone.now()
        form = CommentForm(initial={'created_at': current_time})
    return redirect('home:info_films', id=film_id)


def movie(request, id=None):
    if id is None:
        film_mv = TapFilm.objects.order_by('-ngaychieu').first()
    else:
        film_mv = get_object_or_404(TapFilm, pk=id)
    tap_film = film_mv
    film_cm = tap_film.TenFilm
    total_comments = film_cm.comment_set.count()
    comments = film_cm.comment_set.order_by('-id')
    
    if id is not None:
        increment_view_count(id)
    # Phân trang cho danh sách bình luận
    paginator = Paginator(comments, 6)  # Chia danh sách bình luận thành các trang, mỗi trang có tối đa 10 bình luận
    page_number = request.GET.get('page')  # Lấy số trang từ query string
    page_obj = paginator.get_page(page_number)  # Lấy đối tượng trang hiện tại
    
    film_id = film_mv.TenFilm_id
    all_tap = TapFilm.objects.filter(TenFilm_id=film_id).order_by('-ngaychieu')
    previous_tap = all_tap.filter(ngaychieu__lt=film_mv.ngaychieu).first()
    is_first_tap = all_tap.last() == film_mv
    next_tap = TapFilm.objects.filter(TenFilm_id=film_id, ngaychieu__gt=film_mv.ngaychieu).order_by('ngaychieu').first()
    average_rating = film_cm.ratefilm_set.aggregate(Avg('rating'))['rating__avg']
    total_votes = film_cm.ratefilm_set.count()
    
    return render(request, 'home/movie.html', {
        "film_mv": film_mv,
        "all_tap": all_tap,
        "film_id": film_id,
        "previous_tap": previous_tap,
        "is_first_tap": is_first_tap,
        "next_tap_id": next_tap.id if next_tap else None,
        'total_comments': total_comments,
        'comments': page_obj,  # Truyền đối tượng trang đã phân trang
        'average_rating': average_rating,
        'total_votes': total_votes,
    })



def post_comment_movie(request, tap_film_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_content = form.cleaned_data['comment']
            user_profile = None
            user = request.user
            if user.is_authenticated:
                if hasattr(user, 'userprofile'):
                    user_profile = user.userprofile
                elif user.email:
                    user_profile = UserProfile.objects.create(user=user, account_name=user.username, email=user.email)
            current_time = timezone.now()
            new_comment = Comment.objects.create(film_cm_id=tap_film_id, user_profile=user_profile, comment=comment_content, created_at=current_time)
            messages.success(request, 'Bình luận của bạn đã được gửi.') 
            # Chuyển hướng trang đến URL hiện tại
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
    else:
        current_time = timezone.now()
        form = CommentForm(initial={'created_at': current_time})
    return redirect('home:movie', id=tap_film_id)





def rate_film(request, film_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            film = Film.objects.get(pk=film_id)
            user_profile = request.user.userprofile

            # Kiểm tra xem người dùng đã đánh giá phim này trước đó chưa
            try:
                rate_film = RateFilm.objects.get(film=film, user_profile=user_profile)
                rate_film.rating = rating
                rate_film.save()
            except RateFilm.DoesNotExist:
                RateFilm.objects.create(film=film, user_profile=user_profile, rating=rating)
                
            messages.success(request, 'Cảm ơn bạn đã đánh giá!')
        else:
            messages.error(request, 'Giá trị đánh giá không hợp lệ')
    
    return HttpResponseRedirect(reverse('home:info_films', args=[film_id])) 



def toggle_follow(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    if request.method == 'POST':
        # Kiểm tra trạng thái hiện tại và thay đổi nó
        if film.follow:
            film.follow = False
        else:
            film.follow = True
        film.save()
    return redirect('home:info_films', id=film_id)

    
def search(request):
    query = request.GET.get('search', '')
    films = Film.objects.filter(title__icontains=query)
    return render(request, 'home/search_results.html', {'films': films, 'query': query}) 



from django.shortcuts import render, redirect
from .models import TapFilm,Film
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg,Count,Sum 


# Create your views here.
def sapchieu(request):
    list_tapfilm_first = get_first_episode_dates()
    current_datetime = timezone.now()
    list_sapchieu = []
    for film, ngay_chieu in list_tapfilm_first.items():
        if ngay_chieu > current_datetime:
            list_sapchieu.append(film)
    # Chuyển đổi danh sách các đối tượng Film thành một queryset
    queryset_sapchieu = Film.objects.filter(pk__in=[film.pk for film in list_sapchieu])
    return render(request, 'chedule/sapchieu.html', {"list_sapchieu": queryset_sapchieu})

def get_first_episode_dates():
    first_episodes = {}
    films = Film.objects.all()
    for film in films:
        first_episode = TapFilm.objects.filter(TenFilm=film).order_by('ngaychieu').first()
        if first_episode:
            first_episodes[film] = first_episode.ngaychieu
    return first_episodes



def get_last_completed_films():
    last_films = []
    films = Film.objects.all()
    for film in films:
        last_episode = TapFilm.objects.filter(TenFilm=film).order_by('-ngaychieu').first()
        if last_episode:
            next_week = last_episode.ngaychieu + timedelta(days=7)
            if next_week < timezone.now():
                last_films.append(film)
    return last_films

def hoanthanh(request):
    last_films = get_last_completed_films()
    return render(request, 'chedule/hoanthanh.html', {"last_films": last_films})

def dangchieu(request):
    last_list = get_last_list_tap()
    queryset_dangchieu = [episode.TenFilm for episode in last_list]
    return render(request, 'chedule/dangchieu.html',{"last_list": queryset_dangchieu})


def get_last_list_tap():
    last_episodes = []
    films = Film.objects.all()
    for film in films:
        last_episode = TapFilm.objects.filter(TenFilm=film).order_by('-ngaychieu').first()
        if last_episode:
            if last_episode.ngaychieu < timezone.now():
                next_week = last_episode.ngaychieu + timedelta(days=7)
                if next_week > timezone.now():
                    last_episodes.append(last_episode)
            else:
                last_week = last_episode.ngaychieu - timedelta(days=7)
                if last_week < timezone.now():
                    last_episodes.append(last_episode)
    return last_episodes
                

def get_last_episode_dates_film():
    last_episodes = []
    films = Film.objects.all()
    for film in films:
        last_episode = TapFilm.objects.filter(TenFilm=film).order_by('-ngaychieu').first()
        if last_episode:
            last_episodes.append(last_episode)
    return last_episodes

def schedule():
    schedule = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],   
        'Saturday': [],
        'Sunday': [],
    }   
    last_episodes = get_last_episode_dates_film()
    for episode in last_episodes:
        film = episode.TenFilm
        ngay_chieu = episode.ngaychieu
        weekday = ngay_chieu.strftime('%A')
        film_details = {
            'id': film.id,
            'title': film.title,
            'sub_title': film.sub_title,
            'gioithieu': film.gioithieu,
            'theloai': film.theloai,
            'hinhanh': film.hinhanh,
            'banner': film.banner,
            'tap_films': [{'tentap': episode.tentap}],
        }
        schedule[weekday].append({'film': film_details, 'ngay_chieu': ngay_chieu})
    return schedule

def lichchieu(request):
    schedule_data = schedule() 
    return render(request, 'chedule/lichchieu.html', {'schedule': schedule_data})



def get_high_rated_films():
    # Lấy các bộ phim có điểm đánh giá trung bình cao hơn hoặc bằng 4 và sắp xếp theo điểm đánh giá giảm dần
    high_rated_films = Film.objects.annotate(
        average_rating=Avg('ratefilm__rating'),
        total_votes=Count('ratefilm')
    ).filter(average_rating__gte=3).order_by('-average_rating')
    return high_rated_films


def high_rated_films_view(request):
    # Lấy danh sách các bộ phim có điểm đánh giá cao hơn hoặc bằng 4
    high_rated_films = get_high_rated_films()
    context = {
        'high_rated_films': high_rated_films
    }
    return render(request, 'chedule/dangxem.html', context)



    
def top_10_most_viewed_films(request):
    # Lấy ra 10 bộ phim có số lượt xem cao nhất
    top_10_films = Film.objects.all()[:10]
    # Tạo danh sách các tuple chứa thông tin về bộ phim và tổng số lượt xem
    films_with_views = []
    for film in top_10_films:
        # Lấy tất cả các tập phim của bộ phim
        tap_films = film.tapfilm_set.all()
        # Tính tổng số lượt xem của các tập phim
        total_views = tap_films.aggregate(Sum('view_count'))['view_count__sum'] or 0
        films_with_views.append((film, total_views))
    
    top_10_films = Film.objects.annotate(total_views=Sum('tapfilm__view_count')).order_by('-total_views')[:10]
    context = {
        'films_with_views': films_with_views,
        'top_10_films': top_10_films,   
    }
    return render(request, 'chedule/bxh.html', context)





def followed_films(request):
    followed_films = Film.get_followed_films()
    return render(request, 'chedule/follow.html', {'followed_films': followed_films})
def confirm_unfollow(request, film_id):
    film = Film.objects.get(pk=film_id)
    return render(request, 'chedule/confirm_unfollow.html', {'film': film})
def unfollow(request, film_id):
    if request.method == 'POST':
        film = Film.objects.get(pk=film_id)
        film.follow = False
        film.save()
    return redirect('chedule:followed_films')   




def history(request):
    return render(request, 'chedule/history.html')
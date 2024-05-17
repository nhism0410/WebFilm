from django.db import models
from category.models import Category
from login.models import UserProfile
from django.utils import timezone

# Create your models here.

class Film(models.Model):
    title = models.CharField(max_length = 255, blank = False, null = False) 
    sub_title = models.CharField(max_length = 255, blank = False, null = False)
    gioithieu = models.TextField()
    theloai = models.ForeignKey(Category, on_delete=models.CASCADE)
    hinhanh = models.ImageField(null=True, upload_to='image')
    banner = models.ImageField(null=True, upload_to='banner')
    follow = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    @property
    def total_episodes(self):
        # tính tổng số tập của bộ phim này
        return self.tapfilm_set.count()
    
    def get_year(self):
        # Lấy tập phim đầu tiên
        first_episode = self.tapfilm_set.order_by('ngaychieu').first()
        if first_episode:
            return first_episode.ngaychieu.year
        else:
            return None
        
    def latest_episode(self):
        # Lấy tập mới nhất
        latest_episode = self.tapfilm_set.order_by('-ngaychieu').first()
        if latest_episode:
            return latest_episode.tentap
        else:
            return None
        
        
    def latest_episode_id(self):
        # Lấy tập mới nhất
        latest_episode = self.tapfilm_set.order_by('-ngaychieu').first()
        if latest_episode:
            return latest_episode.id
        else:
            return None
        
    def all_episodes(self):
        # Lấy danh sách tất cả các tập phim của bộ phim
        return self.tapfilm_set.all()
    
    
    @classmethod
    def get_followed_films(cls):
        return cls.objects.filter(follow=True)
     





class Comment(models.Model):
    film_cm = models.ForeignKey(Film, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.comment

    def save(self, *args, **kwargs):
        # Nếu biệt danh không được cung cấp và user_profile không tồn tại
        if not self.user_profile and not self.user_profile_id:
            # Kiểm tra xem user_profile của user hiện tại có tồn tại không
            if hasattr(self, 'user') and self.user.userprofile:
                self.user_profile = self.user.userprofile
        super().save(*args, **kwargs)
    
    
    
    
class RateFilm(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.user_profile} rated {self.film} {self.rating}"

    class Meta:
        unique_together = ['film', 'user_profile'] 
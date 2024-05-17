from django.db import models
from home.models import Film
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class TapFilm(models.Model):
    TenFilm = models.ForeignKey(Film, on_delete=models.CASCADE)
    video = models.FileField(null=False, upload_to='video')
    tentap = models.CharField(max_length= 255, null= False, blank = False)
    ngaychieu = models.DateTimeField()
    view_count = models.IntegerField(default=0)
    
    def __str__(self): 
        return self.tentap
    
    def save(self, *args, **kwargs):
        if not self.ngaychieu:
            tap_truoc = TapFilm.objects.filter(TenFilm=self.TenFilm).order_by('-ngaychieu').first()
            if tap_truoc:
                ngay_moi = tap_truoc.ngaychieu + timezone.timedelta(days=1)
                self.ngaychieu = ngay_moi.replace(hour=10, minute=0, second=0)
            else:
                self.ngaychieu = timezone.datetime.now().replace(hour=10, minute=0, second=0)
        super().save(*args, **kwargs)
        
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        # Kiểm tra nếu ngày chiếu đã được cung cấp và nếu không, raise ValidationError
        if not self.ngaychieu:
            raise ValidationError({'ngaychieu': 'Ngày chiếu không được trống.'})
        
    

from django.shortcuts import render,redirect, get_object_or_404
from .forms import RegistrationForm
from django.http import FileResponse
from django.conf import settings
import os
from django.http import Http404
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile,MuaGoi
from datetime import date,timedelta,datetime
# Create your views here.


def register(request):
    success = False  
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            success = True  
            # return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'login/register.html', {'form': form, 'success': success})  


def user_login(request):
    error_message = None
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username_login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/') 
            else:
                error_message = "Tài khoản hoặc mật khẩu không đúng."
        else:
            # Xử lý các lỗi cụ thể của biểu mẫu (nếu cần)
            pass
    else:
        form = UserLoginForm()
    return render(request, 'login/login.html', {'form': form, 'error_message': error_message})




def media_serve(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    raise Http404


def logout_User(request):
    logout(request)
    return redirect('/')



def thongbao(request):
    return render(request, 'login/thongbao.html')


@login_required
def profile(request):
    try:
        # Lấy hoặc tạo thông tin profile của user
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Nếu UserProfile không tồn tại, tạo mới
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if form.has_changed():
                changed_data = form.cleaned_data
                for field, value in changed_data.items():
                    setattr(user_profile, field, value)
                user_profile.save()
                return redirect('login:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'login/profile.html', {'form': form})

def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        # Lấy đối tượng UserProfile của user hiện tại
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Lưu hình ảnh avatar mới
        user_profile.avatar = request.FILES['avatar']
        user_profile.save()
        
        # Chuyển hướng lại đến trang profile sau khi cập nhật thành công
        return redirect('login:profile')
    else:
        # Nếu không có dữ liệu hình ảnh hoặc là phương thức GET, chuyển hướng về trang profile
        return redirect('login:profile')
    


def muagoi(request):
    if request.method == 'POST':
        tengoi = request.POST.get('tengoi')
        giagoi = request.POST.get('giagoi')
        thoihan = request.POST.get('thoihan')
        phuongthucthanhtoan = request.POST.get('phuongthucthanhtoan')
        ngaymuagoi = request.POST.get('ngaymuagoi')
        
        # Chuyển đổi định dạng ngày tháng từ "April 16, 2025" sang "YYYY-MM-DD"
        ngaymuagoi = datetime.strptime(ngaymuagoi, "%B %d, %Y").strftime("%Y-%m-%d")

        # Lấy user_profile từ request
        user_profile = request.user.userprofile

        # Tạo một đối tượng MuaGoi mới và lưu vào database
        mua_goi = MuaGoi.objects.create(
            user_profile=user_profile,
            tengoi=tengoi,
            giagoi=giagoi,
            thoihan=thoihan,
            phuongthucthanhtoan=phuongthucthanhtoan,
            ngaymuagoi=ngaymuagoi,
        )

        # Redirect hoặc render view bạn muốn sau khi gửi thành công
        return redirect('home:home')
    
    # Nếu không phải phương thức POST, trả về một response mặc định hoặc render một view khác
    return render(request, 'login/muagoi.html')


def process_thanhtoan(request):
    if request.method == 'POST':
        ten_goi = request.POST.get('ten_goi')
        gia_goi = request.POST.get('gia_goi')
        phuong_thuc = request.POST.get('payment_choice')
    gia_goi = float(gia_goi) if gia_goi else 0.0
    thoi_han_goi = [
            (0, '01 THÁNG - TỰ ĐỘNG GIA HẠN'),
            (1, '01 THÁNG'),
            (2, '03 THÁNG'),    
            (3, '06 THÁNG'),
            (4, '12 THÁNG'),
        ]   
    phuong_thuc_thanh_toan =[
        (0, 'Ví điện tử ShopeePay'),
        (1, 'Ví điện tử ZaloPay'),
        (2, 'Ví MoMo'),
    ]
    thoi_han_goi = [(index, thoi_han, '{:.3f}'.format(gia_goi * index)) if index > 0 else (index, thoi_han, '{:.3f}'.format(gia_goi)) for index, thoi_han in thoi_han_goi]
    context = {
        'ten_goi': ten_goi,
        'gia_goi': gia_goi,
        'thoi_han_goi': thoi_han_goi,
        'phuong_thuc_thanh_toan': phuong_thuc_thanh_toan,
        'phuong_thuc': phuong_thuc,
    }
    return render(request, 'login/process_thanhtoan.html', context)
    

    
def thanhtoan(request):
    if request.method == 'POST':
        ten_goi = request.POST.get('ten_goi')
        gia_goi = request.POST.get('gia_goi')
        phuong_thuc = request.POST.get('phuong_thuc')
        thoi_han = request.POST.get('thoi_han')
        gia = request.POST.get('gia')
        
        
        # Xử lý dữ liệu ở đây nếu cần
        ky_thanh_toan_tiep_theo = None
        if thoi_han[:2] == '01':
            ky_thanh_toan_tiep_theo = date.today() + timedelta(days=30)
        elif thoi_han[:2] == '03':
            ky_thanh_toan_tiep_theo = date.today() + timedelta(days=90)
        elif thoi_han[:2] == '06':
            ky_thanh_toan_tiep_theo = date.today() + timedelta(days=180)
        elif thoi_han[:2] == '12':
            ky_thanh_toan_tiep_theo = date.today() + timedelta(days=365)
        
        user_profile = request.user.userprofile
        current_date = date.today()
        context = {
            'user_profile': user_profile,
            'current_date': current_date,
            'ten_goi': ten_goi,
            'gia_goi': gia_goi,
            'phuong_thuc': phuong_thuc,
            'thoi_han': thoi_han,
            'gia': gia,
            'ky_thanh_toan_tiep_theo': ky_thanh_toan_tiep_theo,
        }
        return render(request, 'login/thanhtoan.html', context)

    

def user_mua_goi(request):
    # Lấy thông tin gói đã mua của người dùng hiện tại
    muagoi_list = MuaGoi.objects.filter(user_profile=request.user.userprofile)
    
    # Truyền danh sách các gói đã mua vào template
    context = {'muagoi_list': muagoi_list}
    
    return render(request, 'login/user_mua_goi.html', context)









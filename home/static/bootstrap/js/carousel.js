

function showDay(day) {
  // Ẩn tất cả các div chứa active
  document.querySelectorAll('.day-container').forEach(function(dayContainer) {
    dayContainer.style.display = 'none';  
  });
  // Hiển thị div chứa phim của ngày được chọn
  document.getElementById(day).style.display = 'block'; 
  // Thay đổi màu sắc của nút được nhấp vào
  document.querySelectorAll('.btn').forEach(function(btn) {
    btn.classList.remove('active'); // Loại bỏ lớp 'active' khỏi tất cả các nút
  });
  document.getElementById('btn-' + day.toLowerCase()).classList.add('active'); // Thêm lớp 'active' vào nút được nhấp vào
}


  var timeout;

function showDropdown() {
  clearTimeout(timeout);
  document.getElementById("myDropdownMenu").classList.add("show");
}

function hideDropdown() {
  timeout = setTimeout(function() {
    document.getElementById("myDropdownMenu").classList.remove("show");
  }, 1000); // Khoảng thời gian 1 giây
}
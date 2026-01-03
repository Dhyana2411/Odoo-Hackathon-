// Navigation and common functionality for HRMS dashboard

// Check if user is logged in
function checkAuth() {
  const currentUser = JSON.parse(localStorage.getItem("currentUser"));
  if (!currentUser) {
    alert("Please log in first");
    window.location.href = "sign in.html";
    return null;
  }
  return currentUser;
}

// Logout function
function logout() {
  if (confirm("Are you sure you want to logout?")) {
    localStorage.removeItem("currentUser");
    window.location.href = "sign in.html";
  }
}

// Navigation functions
function navigateToEmployees() {
  window.location.href = "After Sign in.html";
}

function navigateToAttendance() {
  const user = JSON.parse(localStorage.getItem("currentUser"));
  if (user && (user.role === "HR" || user.role === "HR / Admin")) {
    window.location.href = "attendances list of Admin.html";
  } else {
    window.location.href = "attendances list of employee.html";
  }
}

function navigateToTimeOff() {
  window.location.href = "Timeoff.html";
}

function navigateToProfile() {
  window.location.href = "My Profile for Admin.html";
}

// Initialize page with user info
function initializePage() {
  const user = checkAuth();
  if (!user) return;

  // Update company logo/name if exists
  const companyElements = document.querySelectorAll('.navbar-brand');
  companyElements.forEach(el => {
    if (user.company) {
      el.textContent = user.company;
    }
  });

  // Update user name in profile areas
  const userNameElements = document.querySelectorAll('.employee-name-panel, .user-name');
  userNameElements.forEach(el => {
    el.textContent = user.name;
  });

  return user;
}

// Avatar dropdown functionality
function initializeAvatarDropdown() {
  const avatarBtn = document.getElementById("avatarBtn");
  const avatarDropdown = document.getElementById("avatarDropdown");

  if (avatarBtn && avatarDropdown) {
    avatarBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      avatarDropdown.style.display =
        avatarDropdown.style.display === "block" ? "none" : "block";
    });

    document.addEventListener("click", () => {
      avatarDropdown.style.display = "none";
    });
  }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
  initializePage();
  initializeAvatarDropdown();
});
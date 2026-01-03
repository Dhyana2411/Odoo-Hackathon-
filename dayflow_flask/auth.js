let selectedRole = null;

// API Base URL - Change this when deploying
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5000' 
    : 'https://your-app-name.onrender.com'; // Update with your deployment URL

function selectRole(role, btn) {
  selectedRole = role;
  document.querySelectorAll(".role-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

function togglePassword(inputId) {
  const input = document.getElementById(inputId);
  const showPass = input.nextElementSibling;
  
  if (input.type === "password") {
    input.type = "text";
    showPass.textContent = "🙈";
  } else {
    input.type = "password";
    showPass.textContent = "👁️";
  }
}

function uploadLogo(event) {
  const file = event.target.files[0];
  if (file) {
    console.log("Logo uploaded:", file.name);
    // Handle logo upload logic here
  }
}

async function signUp() {
  const company = document.getElementById("company").value.trim();
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  if (!company || !name || !email || !phone || !password || !confirmPassword) {
    alert("Please fill all fields");
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords don't match");
    return;
  }

  if (!selectedRole) {
    alert("Please select a role");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        company,
        name,
        email,
        phone,
        password,
        role: selectedRole
      })
    });

    const data = await response.json();

    if (data.success) {
      alert(`Account created successfully!\nLogin ID: ${data.loginId}\nRole: ${selectedRole}`);
      window.location.href = "sign in.html";
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (error) {
    console.error('Signup error:', error);
    alert('Network error. Please try again.');
  }
}

async function signIn() {
  const loginId = document.getElementById("loginId").value.trim();
  const password = document.getElementById("password").value;

  if (!loginId || !password) {
    alert("Please enter login ID and password");
    return;
  }

  if (!selectedRole) {
    alert("Please select a role");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        loginId,
        password,
        role: selectedRole
      })
    });

    const data = await response.json();

    if (data.success) {
      localStorage.setItem("currentUser", JSON.stringify(data.user));
      alert(`Login Successful! Welcome ${data.user.name}`);
      
      // Redirect based on role
      if (data.user.role === "hr" || data.user.role === "hr / admin") {
        window.location.href = "After Sign in.html";
      } else {
        window.location.href = "After Sign in.html";
      }
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (error) {
    console.error('Signin error:', error);
    alert('Network error. Please try again.');
  }
}

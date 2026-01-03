let selectedRole = null;

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

function signUp() {
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

  // Generate login ID
  const nameParts = name.split(" ");
  const first = nameParts[0].substring(0, 2).toUpperCase();
  const last = nameParts[1] ? nameParts[1].substring(0, 2).toUpperCase() : "XX";
  const year = new Date().getFullYear();
  const users = JSON.parse(localStorage.getItem("users")) || [];
  const serial = String(users.length + 1).padStart(4, "0");
  const loginId = `OI${first}${last}${year}${serial}`;

  const newUser = {
    company,
    name,
    email,
    phone,
    loginId,
    password,
    role: selectedRole
  };

  users.push(newUser);
  localStorage.setItem("users", JSON.stringify(users));
  
  alert(`Account created successfully!\nLogin ID: ${loginId}\nRole: ${selectedRole}`);
  window.location.href = "sign in.html";
}

function signIn() {
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

  const users = JSON.parse(localStorage.getItem("users")) || [];
  const user = users.find(
    u => u.loginId === loginId &&
         u.password === password &&
         u.role === selectedRole
  );

  if (user) {
    localStorage.setItem("currentUser", JSON.stringify(user));
    alert(`Login Successful! Welcome ${user.name}`);
    
    // Redirect based on role
    if (user.role === "HR" || user.role === "HR / Admin") {
      window.location.href = "After Sign in.html";
    } else {
      window.location.href = "After Sign in.html";
    }
  } else {
    alert("Invalid credentials or role mismatch");
  }
}

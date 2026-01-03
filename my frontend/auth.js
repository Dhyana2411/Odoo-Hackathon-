let selectedRole = null;

function selectRole(role, btn) {
  selectedRole = role;
  document.querySelectorAll(".role-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

function generateUser() {
  const name = document.getElementById("name").value.trim();
  if (!name) {
    alert("Enter employee name");
    return;
  }

  const parts = name.split(" ");
  const first = parts[0].substring(0,2).toUpperCase();
  const last = parts[1] ? parts[1].substring(0,2).toUpperCase() : "XX";

  const year = new Date().getFullYear();
  const users = JSON.parse(localStorage.getItem("users")) || [];
  const serial = String(users.length + 1).padStart(4, "0");

  genLogin.value = `OI${first}${last}${year}${serial}`;
  genPass.value = Math.random().toString(36).slice(-8);
}

function saveUser() {
  if (!selectedRole) {
    alert("Please select role");
    return;
  }

  if (!genLogin.value || !genPass.value) {
    alert("Generate Login ID & Password first");
    return;
  }

  const users = JSON.parse(localStorage.getItem("users")) || [];

  users.push({
    company: company.value,
    name: name.value,
    email: email.value,
    phone: phone.value,
    loginId: genLogin.value,
    password: genPass.value,
    role: selectedRole
  });

  localStorage.setItem("users", JSON.stringify(users));
  alert("User created successfully!");
  window.location.href = "index.html";
}

function login() {
  if (!selectedRole) {
    alert("Please select role");
    return;
  }

  const users = JSON.parse(localStorage.getItem("users")) || [];
  const user = users.find(
    u => u.loginId === loginId.value &&
         u.password === password.value &&
         u.role === selectedRole
  );

  if (user) {
    localStorage.setItem("currentUser", JSON.stringify(user));
    alert(`Login Successful (${user.role})`);
  } else {
    alert("Invalid credentials or role");
  }
}

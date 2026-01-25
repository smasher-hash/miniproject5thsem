// Scroll to form section
function scrollToForm() {
  document.getElementById('form').scrollIntoView({ behavior: 'smooth' });
}

// Show simple crop recommendation
function showRecommendation(event) {
  event.preventDefault();
  const district = document.getElementById('district').value;
  const crop = document.getElementById('crop').value;

  const message = `For ${crop} in ${district}: Ensure proper irrigation and check for pest activity this week.`;
  document.getElementById('output').textContent = message;
}


//submission
document.addEventListener('DOMContentLoaded', () => {
  const user = JSON.parse(localStorage.getItem('user'));
  const welcomeEl = document.getElementById('welcome-message');

  if (user) {
    welcomeEl.textContent = `Welcome, ${user.name}!`;
  } else {
    welcomeEl.textContent = "Welcome to Smart Krishi Portal!";
  }
});

document.getElementById('signup-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const name = document.getElementById('signup-name').value;
  const email = document.getElementById('signup-email').value;
  const password = document.getElementById('signup-password').value;

  // Simulate successful registration
  if(name && email && password) {
    // Optional: store user info (not secure, demo purpose only)
    localStorage.setItem('user', JSON.stringify({ name, email }));

    // Redirect to main site
    window.location.href = 'main.html';
  } else {
    alert('Please fill in all fields.');
  }
});
  function toggleMenu() {
    var menu = document.getElementById("menu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  }

function logout() {
  localStorage.removeItem('user');
  window.location.href = 'login.html';
}




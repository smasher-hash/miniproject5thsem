// Toggle between login and signup forms
document.getElementById('show-login').addEventListener('click', () => {
  document.getElementById('login-form').classList.add('active');
  document.getElementById('signup-form').classList.remove('active');
  toggleButtonState('login');
});

document.getElementById('show-signup').addEventListener('click', () => {
  document.getElementById('signup-form').classList.add('active');
  document.getElementById('login-form').classList.remove('active');
  toggleButtonState('signup');
});

function toggleButtonState(active) {
  document.getElementById('show-login').classList.toggle('active', active === 'login');
  document.getElementById('show-signup').classList.toggle('active', active === 'signup');
}

// Google Translate Init
 function googleTranslateElementInit() {
  new google.translate.TranslateElement(
    {pageLanguage: 'en,hi,ta,te,ml,kn,gu,pa,bn,mr,or'},
     'google_translate_element'
   );
}

//submit handler
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


document.addEventListener('DOMContentLoaded', () => {
  const user = JSON.parse(localStorage.getItem('user'));
  const welcomeEl = document.getElementById('welcome-message');

  if (user) {
    welcomeEl.textContent = `Welcome, ${user.name}!`;
  } else {
    welcomeEl.textContent = "Welcome to Smart Krishi Portal!";
  }
});


document.getElementById('login-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  if (email && password) {
    const storedUser = JSON.parse(localStorage.getItem('user'));

    if (storedUser && storedUser.email === email) {
      window.location.href = 'main.html';
    } else {
      alert('User not found or email does not match.');
    }
  } else {
    alert('Please enter both email and password.');
  }
});

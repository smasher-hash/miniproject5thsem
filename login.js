// // Toggle between login and signup forms
// document.getElementById('show-login').addEventListener('click', () => {
//   document.getElementById('login-form').classList.add('active');
//   document.getElementById('signup-form').classList.remove('active');
//   toggleButtonState('login');
// });

// document.getElementById('show-signup').addEventListener('click', () => {
//   document.getElementById('signup-form').classList.add('active');
//   document.getElementById('login-form').classList.remove('active');
//   toggleButtonState('signup');
// });

// function toggleButtonState(active) {
//   document.getElementById('show-login').classList.toggle('active', active === 'login');
//   document.getElementById('show-signup').classList.toggle('active', active === 'signup');
// }

// // Google Translate Init
//  function googleTranslateElementInit() {
//   new google.translate.TranslateElement(
//     {pageLanguage: 'en,hi,ta,te,ml,kn,gu,pa,bn,mr,or'},
//      'google_translate_element'
//    );
// }

// //submit handler
// document.getElementById('signup-form').addEventListener('submit', function(e) {
//   e.preventDefault();

//   const name = document.getElementById('signup-name').value;
//   const email = document.getElementById('signup-email').value;
//   const password = document.getElementById('signup-password').value;

//   // Simulate successful registration
//   if(name && email && password) {
//     // Optional: store user info (not secure, demo purpose only)
//     localStorage.setItem('user', JSON.stringify({ name, email }));

//     // Redirect to main site
//     window.location.href = 'index.html';
//   } else {
//     alert('Please fill in all fields.');
//   }
// });


// document.addEventListener('DOMContentLoaded', () => {
//   const user = JSON.parse(localStorage.getItem('user'));
//   const welcomeEl = document.getElementById('welcome-message');

//   if (user) {
//     welcomeEl.textContent = `Welcome, ${user.name}!`;
//   } else {
//     welcomeEl.textContent = "Welcome to Smart Krishi Portal!";
//   }
// });


// document.getElementById('login-form').addEventListener('submit', function(e) {
//   e.preventDefault();

//   const email = document.getElementById('login-email').value;
//   const password = document.getElementById('login-password').value;

//   if (email && password) {
//     const storedUser = JSON.parse(localStorage.getItem('user'));

//     if (storedUser && storedUser.email === email) {
//       window.location.href = 'main.html';
//     } else {
//       alert('User not found or email does not match.');
//     }
//   } else {
//     alert('Please enter both email and password.');
//   }
// });



// =====================================
// KRISHIMITRA-AI LOGIN / SIGNUP
// Connected to Flask + MongoDB
// =====================================

// Form elements
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");

const loginButton = document.getElementById("show-login");
const signupButton = document.getElementById("show-signup");

const messageElement = document.getElementById("auth-message");

// Display messages
function showMessage(message, success = false) {
    if (!messageElement) {
        alert(message);
        return;
    }

    messageElement.textContent = message;
    messageElement.style.color = success ? "green" : "red";
}

// Toggle forms
function toggleButtonState(active) {
    loginButton.classList.toggle("active", active === "login");
    signupButton.classList.toggle("active", active === "signup");
}

function showLogin() {
    loginForm.classList.add("active");
    signupForm.classList.remove("active");
    toggleButtonState("login");
    showMessage("");
}

function showSignup() {
    signupForm.classList.add("active");
    loginForm.classList.remove("active");
    toggleButtonState("signup");
    showMessage("");
}

loginButton.addEventListener("click", showLogin);
signupButton.addEventListener("click", showSignup);


// =====================================
// SIGNUP
// =====================================

signupForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("signup-name").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value;

    if (!name || !email || !password) {
        showMessage("Please fill in all fields.");
        return;
    }

    if (password.length < 8) {
        showMessage("Password must contain at least 8 characters.");
        return;
    }

    const submitButton = signupForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        const response = await fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showMessage(result.message, true);

            window.location.href = result.redirect;
        } else {
            showMessage(result.message || "Registration failed.");
        }

    } catch (error) {
        console.error("Signup error:", error);
        showMessage("Unable to connect to the server. Please try again.");
    } finally {
        submitButton.disabled = false;
    }
});


// =====================================
// LOGIN
// =====================================

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    if (!email || !password) {
        showMessage("Please enter both email and password.");
        return;
    }

    const submitButton = loginForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showMessage(result.message, true);

            window.location.href = result.redirect;
        } else {
            showMessage(result.message || "Login failed.");
        }

    } catch (error) {
        console.error("Login error:", error);
        showMessage("Unable to connect to the server. Please try again.");
    } finally {
        submitButton.disabled = false;
    }
});


// =====================================
// GOOGLE TRANSLATE
// =====================================

window.googleTranslateElementInit = function () {
    if (window.google && window.google.translate) {
        new google.translate.TranslateElement(
            {
                pageLanguage: "en"
            },
            "google_translate_element"
        );
    }
};


// =====================================
// SELECT FORM FROM URL
// Example: /login?form=signup
// =====================================

const urlParams = new URLSearchParams(window.location.search);

if (urlParams.get("form") === "signup") {
    showSignup();
} else {
    showLogin();
}

// Get form elements and container
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const signUpErrorDialog = document.querySelector('.sign-up-container .error-dialog');
const signInErrorDialog = document.querySelector('.sign-in-container .error-dialog');

// Event listeners for switching between sign-up and sign-in
signUpButton.addEventListener('click', () => {
  container.classList.add("right-panel-active");
  hideErrorMessage(signUpErrorDialog);
});

signInButton.addEventListener('click', () => {
  container.classList.remove("right-panel-active");
  hideErrorMessage(signInErrorDialog);
});

// Validate registration form
function validateRegistrationForm() {
  const name = document.getElementsByName('name')[0].value;
  const email = document.getElementById('regEmail').value;
  const password = document.getElementById('regPassword').value;

  // Validate email format
  const emailPattern = /[^@]+@[^@]+\.[^@]+/;
  if (!emailPattern.test(email)) {
    showErrorMessage("Invalid email format", signUpErrorDialog);
    return false;
  }

  // Validate password format
  const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
  if (!passwordPattern.test(password)) {
    showErrorMessage("Invalid password format. It should contain at least 8 characters, one uppercase letter, one digit, and one special character.", signUpErrorDialog);
    return false;
  }


  return true;
}

// Validate login form
function validateLoginForm() {
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;

  // Validate email format
  const emailPattern = /[^@]+@[^@]+\.[^@]+/;
  if (!emailPattern.test(email)) {
    showErrorMessage("Invalid email format", signInErrorDialog);
    return false;
  }

  // Validate password format
  const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
  if (!passwordPattern.test(password)) {
    showErrorMessage("Invalid password format", signInErrorDialog);
    return false;
  }

  return true;
}

// Show error message
function showErrorMessage(message, errorDialog) {
  const errorText = errorDialog.querySelector('p');
  errorText.innerText = message;
  errorDialog.style.display = 'block';
}

// Hide error message
function hideErrorMessage(errorDialog) {
  errorDialog.style.display = 'none';
}

// Event listener to hide error message on input change
const inputs = document.querySelectorAll('input');
inputs.forEach((input) => {
  input.addEventListener('input', () => {
    if (container.classList.contains("right-panel-active")) {
      hideErrorMessage(signUpErrorDialog);
    } else {
      hideErrorMessage(signInErrorDialog);
    }
  });
});

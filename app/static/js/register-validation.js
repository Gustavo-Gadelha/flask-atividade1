document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registerForm");

  form.addEventListener("submit", function (event) {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Validate username
    if (username.length < 5) {
      alert("O nome de usuário deve ter pelo menos 5 caracteres.");
      event.preventDefault(); // Prevent form submission
      return;
    }

    // Validate password match
    if (password !== confirmPassword) {
      alert("As senhas não correspondem.");
      event.preventDefault(); // Prevent form submission
      return;
    }
  });
});

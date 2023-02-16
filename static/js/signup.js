function validatePassword(){
    var password = document.getElementById("password")
  , confirm_password = document.getElementById("password-confirmation");

  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
    confirm_password.reportValidity();
    return false;
} else {
    confirm_password.setCustomValidity("");
    return true;
  }

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
}

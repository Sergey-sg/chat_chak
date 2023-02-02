const passwordsInput = document.querySelectorAll('input[type="password"]');
let showPasswordsCheck;

for (let passwordInput of passwordsInput) {
    passwordInput.insertAdjacentHTML('afterend', '<label><input type="checkbox" class="show-password-checkbox"> show password</label>');
}

showPasswordsCheck = document.querySelectorAll('.show-password-checkbox');
for (let showPasswordCheck of showPasswordsCheck) {
    showPasswordCheck.addEventListener('change', (event)=>{
        let showPassword = event.target;
        let passwordInput = showPassword.parentNode.previousSibling;
        if (showPassword.checked) {
            passwordInput.type = 'text';
        } else {
            passwordInput.type = 'password';
        }
    });
}
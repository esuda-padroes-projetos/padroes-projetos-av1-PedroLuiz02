const regexNome = /^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)+$/;
const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const regexSenha = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{6,}$/;
    
function validarInput(input, regex) {
    if (regex.test(input.value)) {
        input.style.border = "2px solid green";
    } else {
        input.style.border = "2px solid red";
        }
}
    
const fullnameInput = document.getElementById("fullname")
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("password");
const confirmSenhaInput = document.getElementById("confirm-password");
    
fullnameInput.addEventListener("input", () => validarInput(fullnameInput, regexNome));
emailInput.addEventListener("input", () => validarInput(emailInput, regexEmail));
senhaInput.addEventListener("input", () => validarInput(senhaInput, regexSenha));
    
confirmSenhaInput.addEventListener("input", () => {
    if (confirmSenhaInput.value === senhaInput.value && senhaInput.value !== "") {
        confirmSenhaInput.style.border = "2px solid green";
    } else {
        confirmSenhaInput.style.border = "2px solid red";
    }
});
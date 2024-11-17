document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.getElementById('overlay');
    const loginContent = document.getElementById('loginContent');
    const formCadastro = document.getElementById('formCadastro');

    // Exibir o overlay e a tela de cadastro
    function mostrarTelaLogin() {
        overlay.classList.add('visible');
        loginContent.classList.remove('hidden');
        document.body.classList.add('no-scroll');
    }

    // Fechar o overlay e a tela de cadastro
    function fecharTelaLogin() {
        overlay.classList.remove('visible');
        loginContent.classList.add('hidden');
        document.body.classList.remove('no-scroll');
    }

    // fecha a tela de login quando clica no botão cadastrar
    formCadastro.addEventListener('submit', function (event) {
        fecharTelaLogin();
    });

    // Inicializar o overlay e a tela de cadastro
    mostrarTelaLogin();
});

let hideTimeout;
const menu = document.getElementById('headerMenu');

function toggleMenu() {
    menu.classList.toggle('active');
    startTimer(); 
}

function startTimer() {
    clearTimeout(hideTimeout);
    hideTimeout = setTimeout(() => {
        menu.classList.remove('active');
    }, 500); 
}

function resetTimer() {
    clearTimeout(hideTimeout);
}
startTimer();

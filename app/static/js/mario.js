const mario = document.querySelector('.mario');
const pipe = document.querySelector('.pipe');
const cloud = document.querySelector('.cloud');
const gameOver = document.querySelector('.game-over');
const restartButton = document.querySelector('.restart');

let gameLoop = null;
let scoreLoop = null;
let score = 0;

function resetScore() {
    score = 0;
    document.querySelector('#score').textContent = score;
}

function startScoreLoop() {
    if (scoreLoop) {
        clearInterval(scoreLoop);
    }

    scoreLoop = setInterval(() => {
        score += 1;
        document.querySelector('#score').textContent = score;
    }, 500);
}

function jump() {
    mario.classList.add('jump');
    setTimeout(() => {
        mario.classList.remove('jump');
    }, 500);
}

async function saveScore() {
    const nickname = localStorage.getItem('nickname');
    if (!nickname) {
        return;
    }

    try {
        await fetch('/api/jogador/pontos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nickname, jogo: 'mario', pontos: score }),
        });
    } catch (error) {
        console.error('Não foi possível salvar a pontuação do Mario.', error);
    }
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp' || event.key === ' ' || event.code === 'Space') {
        jump();
    }
});

document.addEventListener('touchstart', jump);

function finishGame() {
    clearInterval(gameLoop);
    clearInterval(scoreLoop);
    saveScore();

    pipe.style.animation = 'none';
    pipe.style.left = pipe.offsetLeft + 'px';

    mario.style.animation = 'none';
    mario.style.bottom = window.getComputedStyle(mario).bottom;
    mario.src = '/static/img/game-over.png';
    mario.style.width = '70px';
    mario.style.marginLeft = '35px';

    gameOver.style.visibility = 'visible';
}

function startLoop() {
    if (gameLoop) {
        clearInterval(gameLoop);
    }

    gameLoop = setInterval(() => {
        const pipePosition = pipe.offsetLeft;
        const marioPosition = +window.getComputedStyle(mario).bottom.replace('px', '');

        if (pipePosition <= 100 && pipePosition > 0 && marioPosition < 60) {
            finishGame();
            return;
        }
    }, 10);

    startScoreLoop();
}

function restartGame() {
    gameOver.style.visibility = 'hidden';
    resetScore();

    pipe.style.animation = 'pipe-animations 1.5s infinite linear';
    pipe.style.left = '';

    mario.src = '/static/img/mario.gif';
    mario.style.width = '130px';
    mario.style.bottom = '0px';
    mario.style.marginLeft = '';
    mario.style.animation = '';

    cloud.style.left = '';
    startLoop();
}

restartButton.addEventListener('click', restartGame);
startLoop();

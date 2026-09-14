const player = document.getElementById("player");

if (player) {
    const gameIcons = [...document.querySelectorAll(".icone-jogo")];
    const movement = {
        w: [0, -2],
        a: [-2, 0],
        s: [0, 2],
        d: [2, 0],
        ArrowUp: [0, -2],
        ArrowLeft: [-2, 0],
        ArrowDown: [0, 2],
        ArrowRight: [2, 0],
    };

    let playerX = 16;
    let playerY = 76;

    function getClosestGame() {
        const playerBox = player.getBoundingClientRect();
        const playerCenterX = playerBox.left + playerBox.width / 2;
        const playerCenterY = playerBox.top + playerBox.height / 2;
        let closestGame = null;
        let closestDistance = Number.POSITIVE_INFINITY;

        gameIcons.forEach((gameIcon) => {
            const iconBox = gameIcon.getBoundingClientRect();
            const iconCenterX = iconBox.left + iconBox.width / 2;
            const iconCenterY = iconBox.top + iconBox.height / 2;
            const distance = Math.hypot(
                playerCenterX - iconCenterX,
                playerCenterY - iconCenterY,
            );

            if (distance < closestDistance) {
                closestDistance = distance;
                closestGame = gameIcon;
            }
        });

        return closestDistance <= 120 ? closestGame : null;
    }

    function updateSelectedGame() {
        const selectedGame = getClosestGame();

        gameIcons.forEach((gameIcon) => {
            gameIcon.classList.toggle("selecionado", gameIcon === selectedGame);
        });

        return selectedGame;
    }

    updateSelectedGame();

    document.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            const selectedGame = updateSelectedGame();

            if (selectedGame) {
                selectedGame.click();
            }

            return;
        }

        const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
        const direction = movement[key];

        if (!direction) {
            return;
        }

        event.preventDefault();
        playerX = Math.max(3, Math.min(97, playerX + direction[0]));
        playerY = Math.max(3, Math.min(97, playerY + direction[1]));
        player.style.left = `${playerX}%`;
        player.style.top = `${playerY}%`;
        updateSelectedGame();
    });
}
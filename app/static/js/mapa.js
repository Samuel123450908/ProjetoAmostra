const player = document.getElementById("player");
const mapImage = document.querySelector(".map-image");

if (player) {
    const gameIcons = [...document.querySelectorAll(".icone-jogo")];
    const collisionCanvas = document.createElement("canvas");
    const collisionContext = collisionCanvas.getContext("2d", { willReadFrequently: true });
    let mapPixels = null;
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

    function loadCollisionMap() {
        if (!mapImage.complete || !mapImage.naturalWidth) {
            return;
        }

        collisionCanvas.width = mapImage.naturalWidth;
        collisionCanvas.height = mapImage.naturalHeight;
        collisionContext.drawImage(mapImage, 0, 0);
        mapPixels = collisionContext.getImageData(
            0,
            0,
            collisionCanvas.width,
            collisionCanvas.height,
        ).data;
    }

    function isWalkable(x, y) {
        if (!mapPixels) {
            return false;
        }

        const mapBounds = mapImage.parentElement.getBoundingClientRect();
        const candidateX = mapBounds.left + (x / 100) * mapBounds.width;
        const candidateY = mapBounds.top + (y / 100) * mapBounds.height;
        const isOverGameIcon = gameIcons.some((gameIcon) => {
            const iconBounds = gameIcon.getBoundingClientRect();

            return (
                candidateX >= iconBounds.left &&
                candidateX <= iconBounds.right &&
                candidateY >= iconBounds.top &&
                candidateY <= iconBounds.bottom
            );
        });

        if (isOverGameIcon) {
            return true;
        }

        if (x >= 13 && x <= 21 && y >= 74 && y <= 82) {
            return true;
        }

        const pixelX = Math.floor((x / 100) * collisionCanvas.width);
        const pixelY = Math.floor((y / 100) * collisionCanvas.height);

        if (
            pixelX < 0 ||
            pixelX >= collisionCanvas.width ||
            pixelY < 0 ||
            pixelY >= collisionCanvas.height
        ) {
            return false;
        }

        const pixelIndex = (pixelY * collisionCanvas.width + pixelX) * 4;
        const redDifference = mapPixels[pixelIndex] - 251;
        const greenDifference = mapPixels[pixelIndex + 1] - 229;
        const blueDifference = mapPixels[pixelIndex + 2] - 169;

        return (
            redDifference ** 2 +
            greenDifference ** 2 +
            blueDifference ** 2 <=
            75 ** 2
        );
    }

    if (mapImage.complete) {
        loadCollisionMap();
    } else {
        mapImage.addEventListener("load", loadCollisionMap, { once: true });
    }

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
        const nextX = Math.max(3, Math.min(97, playerX + direction[0]));
        const nextY = Math.max(3, Math.min(97, playerY + direction[1]));

        if (isWalkable(nextX, nextY)) {
            playerX = nextX;
            playerY = nextY;
            player.style.left = `${playerX}%`;
            player.style.top = `${playerY}%`;
        }

        updateSelectedGame();
    });
}
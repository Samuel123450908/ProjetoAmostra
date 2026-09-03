document.querySelectorAll(".delete-player").forEach((button) => {
    button.addEventListener("click", async () => {
        const row = button.closest(".player-row");
        const nickname = row.querySelector(".nickname").textContent.trim();

        if (!window.confirm(`Excluir o jogador ${nickname}?`)) {
            return;
        }

        button.disabled = true;

        try {
            const response = await fetch(`/api/jogador/${row.dataset.playerId}`, {
                method: "DELETE",
            });

            if (!response.ok) {
                throw new Error("Não foi possível excluir o jogador.");
            }

            row.remove();
        } catch (error) {
            button.disabled = false;
            window.alert(error.message);
        }
    });
});
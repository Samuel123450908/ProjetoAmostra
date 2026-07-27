const inputNickname = document.getElementById("nickname");
const botaoIniciar = document.getElementById("iniciar");
const botaoGerarNome = document.getElementById("gerar-nome");

async function iniciarJogo() {
    const nickname = inputNickname.value.trim();

    if (!nickname) {
        alert("Digite um nickname.");
        return;
    }

    localStorage.setItem("nickname", nickname);

    try {
        const resposta = await fetch("/api/jogador", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nickname }),
        });

        if (!resposta.ok) {
            console.warn("Falha ao salvar nickname no backend, mas ele foi salvo localmente.");
        }

        window.location.href = "/mapa";
    } catch (erro) {
        console.error(erro);
        window.location.href = "/mapa";
    }
}

async function gerarNickname() {
    const botaoGerarNome = document.getElementById("gerar-nome");

    if (botaoGerarNome) {
        botaoGerarNome.disabled = true;
        botaoGerarNome.textContent = "Gerando...";
    }

    try {
        const resposta = await fetch("https://randomuser.me/api/?inc=name&noinfo");

        if (!resposta.ok) {
            throw new Error("Falha ao buscar nome");
        }

        const dados = await resposta.json();
        const nome = dados.results?.[0]?.name?.first;

        if (nome && inputNickname) {
            inputNickname.value = nome;
        } else {
            throw new Error("Nome não encontrado");
        }
    } catch (erro) {
        console.error(erro);
        if (inputNickname) {
            inputNickname.value = "Jogador";
        }
    } finally {
        if (botaoGerarNome) {
            botaoGerarNome.disabled = false;
            botaoGerarNome.textContent = "Nome aleatório";
        }
    }
}

if (inputNickname) {
    inputNickname.value = localStorage.getItem("nickname") || "";
    inputNickname.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            iniciarJogo();
        }
    });
}

if (botaoIniciar) {
    botaoIniciar.addEventListener("click", iniciarJogo);
}

if (botaoGerarNome) {
    botaoGerarNome.addEventListener("click", gerarNickname);
}
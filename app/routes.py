from flask import jsonify, render_template, request, app
from .models import Jogador

from . import db
from .models import Jogador

@app.route("/api/jogador/pontos", methods=["POST"])
def atualizar_pontos():
    dados = request.get_json(silent=True) or {}

    nickname = str(
        dados.get("nickname") or ""
    ).strip()

    jogo = str(
        dados.get("jogo") or ""
    ).strip().lower()

    pontos = dados.get("pontos")

    if not nickname:
        return jsonify({
            "error": "Nickname é obrigatório."
        }), 400

    if jogo not in {"pacman", "mario", "snake"}:
        return jsonify({
            "error": "Jogo inválido."
        }), 400

    try:
        pontos = int(pontos)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Pontuação inválida."
        }), 400

    jogador = Jogador.query.filter_by(
        nickname=nickname
    ).first()

    if jogador is None:
        jogador = Jogador(
            nickname=nickname,
            pontos_pacman=0,
            pontos_mario=0,
            pontos_snake=0
        )

        db.session.add(jogador)

    if jogo == "pacman":
        jogador.pontos_pacman = max(
            jogador.pontos_pacman or 0,
            pontos
        )

    elif jogo == "mario":
        jogador.pontos_mario = max(
            jogador.pontos_mario or 0,
            pontos
        )

    elif jogo == "snake":
        jogador.pontos_snake = max(
            jogador.pontos_snake or 0,
            pontos
        )

    db.session.commit()

    return jsonify({
        "ok": True,
        "nickname": jogador.nickname,
        "jogo": jogo,
        "pontos": pontos
    }), 200
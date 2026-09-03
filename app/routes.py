from flask import Blueprint, jsonify, render_template, request
from . import db
from .models import Jogador

# Cria o Blueprint para registrar no seu __init__.py ou app.py principal
bp = Blueprint("api", __name__)


def register_routes(app):
    app.register_blueprint(bp)

    app.add_url_rule("/", "inicio", inicio)
    app.add_url_rule("/mapa", "mapa", mapa)
    app.add_url_rule("/snake", "snake", snake)
    app.add_url_rule("/memoria", "jogo_memoria", jogo_memoria)
    app.add_url_rule("/pacman", "pacman", pacman)
    app.add_url_rule("/ranking", "ranking", ranking)


def inicio():
    return render_template("index.html")


def mapa():
    return render_template("mapa.html")


def snake():
    return render_template("snake.html")


def jogo_memoria():
    return render_template("memoria.html")


def pacman():
    return render_template("pacman.html")


def ranking():
    jogadores = Jogador.query.order_by(
        (Jogador.pontos_pacman + Jogador.pontos_mario + Jogador.pontos_snake).desc()
    ).all()
    return render_template("ranking.html", ranking_data=jogadores)


@bp.route("/api/jogador", methods=["POST"])
def criar_jogador():
    dados = request.get_json(silent=True) or {}
    nickname = str(dados.get("nickname") or "").strip()

    if not nickname:
        return jsonify({"error": "Nickname é obrigatório."}), 400
    if len(nickname) > 30:
        return jsonify({"error": "Nickname deve ter no máximo 30 caracteres."}), 400

    jogador = Jogador.query.filter_by(nickname=nickname).first()
    if jogador is None:
        jogador = Jogador(nickname=nickname)
        db.session.add(jogador)
        db.session.commit()

    return jsonify({"ok": True, "nickname": jogador.nickname}), 200


@bp.route("/api/jogador/pontos", methods=["POST"])
def atualizar_pontos():
    dados = request.get_json(silent=True) or {}

    nickname = str(dados.get("nickname") or "").strip()
    jogo = str(dados.get("jogo") or "").strip().lower()
    pontos = dados.get("pontos")

    if not nickname:
        return jsonify({"error": "Nickname é obrigatório."}), 400

    if jogo not in {"pacman", "mario", "snake"}:
        return jsonify({"error": "Jogo inválido."}), 400

    try:
        pontos = int(pontos)
    except (ValueError, TypeError):
        return jsonify({"error": "Pontuação inválida."}), 400

    jogador = Jogador.query.filter_by(nickname=nickname).first()

    if jogador is None:
        jogador = Jogador(
            nickname=nickname,
            pontos_pacman=0,
            pontos_mario=0,
            pontos_snake=0,
        )
        db.session.add(jogador)

    if jogo == "pacman":
        jogador.pontos_pacman = max(jogador.pontos_pacman or 0, pontos)
    elif jogo == "mario":
        jogador.pontos_mario = max(jogador.pontos_mario or 0, pontos)
    elif jogo == "snake":
        jogador.pontos_snake = max(jogador.pontos_snake or 0, pontos)

    db.session.commit()

    return (
        jsonify(
            {
                "ok": True,
                "nickname": jogador.nickname,
                "jogo": jogo,
                "pontos": pontos,
            }
        ),
        200,
    )


@bp.route("/api/jogador/<int:jogador_id>", methods=["DELETE"])
def excluir_jogador(jogador_id):
    jogador = db.session.get(Jogador, jogador_id)

    if jogador is None:
        return jsonify({"error": "Jogador não encontrado."}), 404

    db.session.delete(jogador)
    db.session.commit()

    return jsonify({"ok": True}), 200
import sqlite3
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import desc

from . import db
from .models import Jogador

# Cria o Blueprint para registrar no seu __init__.py ou app.py principal
bp = Blueprint("api", __name__)


def init_scores_db():
    with sqlite3.connect("jogos.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                game_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def register_routes(app):
    init_scores_db()
    app.register_blueprint(bp)

    app.add_url_rule("/", "inicio", inicio)
    app.add_url_rule("/mapa", "mapa", mapa)
    app.add_url_rule("/snake", "snake", snake)
    app.add_url_rule("/mario", "mario", mario)
    app.add_url_rule("/memoria", "jogo_memoria", jogo_memoria)
    app.add_url_rule("/pacman", "pacman", pacman)
    app.add_url_rule("/ranking", "ranking", ranking)


def inicio():
    return render_template("index.html")


def mapa():
    return render_template("mapa.html")


def snake():
    return render_template("snake.html")


def mario():
    return render_template("mario.html")


def jogo_memoria():
    return render_template("memoria.html")


def pacman():
    return render_template("pacman.html")


def ranking():
    jogadores = Jogador.query.order_by(
        desc(
            db.text(
                "pontos_pacman + pontos_mario + pontos_snake"
            )
        )
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
        pontos = int(str(pontos))
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


@bp.route("/v1/scores", methods=["POST"])
def salvar_score_interno():
    dados = request.get_json(silent=True) or {}
    username = str(dados.get("username") or "").strip()
    game_name = str(dados.get("game_name") or "").strip()
    score = dados.get("score")

    if not username or not game_name:
        return jsonify({"error": "username e game_name são obrigatórios."}), 400

    try:
        score = int(str(score))
    except (TypeError, ValueError):
        return jsonify({"error": "score inválido."}), 400

    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    with sqlite3.connect("jogos.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scores (username, game_name, score, created_at) VALUES (?, ?, ?, ?)",
            (username, game_name, score, created_at),
        )
        conn.commit()

    return jsonify({"message": "Pontuação salva com sucesso!"}), 201


@bp.route("/v1/scores", methods=["GET"])
def listar_scores_interno():
    with sqlite3.connect("jogos.db") as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, username, game_name, score, created_at FROM scores ORDER BY id DESC"
        ).fetchall()

    scores = [dict(row) for row in rows]
    return jsonify({"scores": scores}), 200


@bp.route("/v1/scores/<username>", methods=["GET"])
def buscar_score_por_usuario(username):
    username = username.strip()

    with sqlite3.connect("jogos.db") as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, username, game_name, score, created_at FROM scores WHERE username = ? ORDER BY id DESC",
            (username,),
        ).fetchall()

    if not rows:
        return jsonify({"error": "Usuário não encontrado."}), 404

    scores = [dict(row) for row in rows]
    return jsonify({"username": username, "scores": scores}), 200


@bp.route("/v1/ranking", methods=["GET"])
def ranking_api():
    jogadores = Jogador.query.all()
    payload = []

    for jogador in jogadores:
        payload.extend(
            [
                {"id": jogador.id, "nickname": jogador.nickname, "jogo": "pacman", "pontos": jogador.pontos_pacman or 0},
                {"id": jogador.id, "nickname": jogador.nickname, "jogo": "mario", "pontos": jogador.pontos_mario or 0},
                {"id": jogador.id, "nickname": jogador.nickname, "jogo": "snake", "pontos": jogador.pontos_snake or 0},
            ]
        )

    payload.sort(key=lambda item: item["pontos"], reverse=True)

    return jsonify({"ranking": payload}), 200
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect("jogos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            game_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Inicializa o banco ao rodar o script
init_db()

# Modelo de dados que a API espera receber
class ScoreSchema(BaseModel):
    username: str
    game_name: str
    score: int

# Rota para SALVAR uma nova pontuação (POST)
@app.post("/v1/scores", status_code=201)
def save_score(data: ScoreSchema):
    conn = sqlite3.connect("jogos.db")
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat() + "Z"
    
    cursor.execute(
        "INSERT INTO scores (username, game_name, score, created_at) VALUES (?, ?, ?, ?)",
        (data.username, data.game_name, data.score, now)
    )
    conn.commit()
    conn.close()
    
    return {"message": "Pontuação salva com sucesso!"}

# Rota para RECUPERAR todas as pontuações (GET)
@app.get("/v1/scores")
def get_scores():
    conn = sqlite3.connect("jogos.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, game_name, score, created_at FROM scores")
    rows = cursor.fetchall()
    conn.close()
    
    # Formatar os resultados em uma lista de dicionários
    scores = [
        {
            "id": row[0],
            "username": row[1],
            "game_name": row[2],
            "score": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]
    
    return {"scores": scores}
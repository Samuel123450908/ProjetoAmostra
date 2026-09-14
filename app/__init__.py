from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlite3 import connect, Error
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware para habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para inicializar o banco de dados
def init_db():
    with connect("jogos.db") as conn:
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

# Inicializa o banco ao iniciar o aplicativo
@app.on_event("startup")
def startup_event():
    init_db()

# Modelo de dados que a API espera receber
class ScoreSchema(BaseModel):
    username: str
    game_name: str
    score: int

# Rota para SALVAR uma nova pontuação (POST)
@app.post("/v1/scores", status_code=201)
def save_score(data: ScoreSchema):
    try:
        now = datetime.utcnow().isoformat() + "Z"
        with connect("jogos.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scores (username, game_name, score, created_at) VALUES (?, ?, ?, ?)",
                (data.username, data.game_name, data.score, now)
            )
            conn.commit()
        return {"message": "Pontuação salva com sucesso!"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar pontuação: {str(e)}")
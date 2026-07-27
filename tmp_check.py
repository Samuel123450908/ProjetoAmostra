import os
import tempfile
from app import create_app
from app.models import Jogador

tmp = tempfile.mkdtemp()
app = create_app({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': f"sqlite:///{os.path.join(tmp, 'test.db')}",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})
client = app.test_client()
print('create', client.post('/api/jogador', json={'nickname': 'Teste'}).status_code)
print('score', client.post('/api/jogador/pontos', json={'nickname': 'Teste', 'jogo': 'pacman', 'pontos': 125}).status_code)
print('stored', Jogador.query.filter_by(nickname='Teste').first().pontos_pacman)

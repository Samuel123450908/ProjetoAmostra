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

print('POST /api/jogador ->', client.post('/api/jogador', json={'nickname': 'teste'}).status_code)
resp = client.post('/api/jogador/pontos', json={'nickname': 'teste', 'jogo': 'pacman', 'pontos': 123})
print('POST /api/jogador/pontos ->', resp.status_code, resp.get_json())
print('Player points', Jogador.query.filter_by(nickname='teste').first().pontos_pacman)

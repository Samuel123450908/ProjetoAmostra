import os
import tempfile
import unittest

from app import create_app, db
from app.models import Jogador


class AppDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.join(self.temp_dir, 'test.db')}",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            }
        )
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_ranking_and_player_creation(self):
        response = self.client.post(
            "/api/jogador",
            json={"nickname": "Teste"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        jogador = Jogador.query.filter_by(nickname="Teste").first()
        self.assertIsNotNone(jogador)

        ranking_response = self.client.get("/ranking")
        self.assertEqual(ranking_response.status_code, 200)
        self.assertIn(b"Teste", ranking_response.data)

    def test_update_score_for_pacman(self):
        self.client.post(
            "/api/jogador",
            json={"nickname": "Teste"},
            content_type="application/json",
        )

        response = self.client.post(
            "/api/jogador/pontos",
            json={"nickname": "Teste", "jogo": "pacman", "pontos": 125},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        jogador = Jogador.query.filter_by(nickname="Teste").first()
        self.assertEqual(jogador.pontos_pacman, 125)


if __name__ == "__main__":
    unittest.main()

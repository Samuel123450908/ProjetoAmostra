from app import db


class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nickname = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    pontos_pacman = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    pontos_mario = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    pontos_snake = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    @property
    def pacman(self):
        return self.pontos_pacman

    @property
    def mario(self):
        return self.pontos_mario

    @property
    def snake(self):
        return self.pontos_snake

    def __repr__(self):
        return f"<Jogador {self.nickname}>"
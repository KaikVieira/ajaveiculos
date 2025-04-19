from app import db
from sqlalchemy.orm import validates
from datetime import datetime

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200))
    ano = db.Column(db.Integer, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    
    imagens = db.relationship(
        'ImagemCarro',
        backref='carro',
        lazy=True,
        cascade='all, delete-orphan'
    )

    @validates('ano')
    def validate_ano(self, key, ano):
       
        current_year = datetime.now().year + 1
        if not 1900 <= int(ano) <= current_year:
            raise ValueError("Ano inválido")
        return ano

    def __repr__(self):
        return f'<Carro {self.nome} | {self.marca} {self.modelo} | {self.ano}>'

class ImagemCarro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_imagem = db.Column(db.String(500), nullable=False, unique=True)
    carro_id = db.Column(db.Integer, db.ForeignKey('carro.id', ondelete='CASCADE'), nullable=False)

    @validates('url_imagem')
    def validate_url_imagem(self, key, url_imagem):
     
        extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        if not any(ext in url_imagem.lower() for ext in extensoes_permitidas):
            raise ValueError("Formato de imagem inválido")
        return url_imagem

    def __repr__(self):
        return f'<ImagemCarro {self.url_imagem}>'


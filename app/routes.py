import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from app import db
from app.models import Carro, ImagemCarro
import cloudinary.uploader

main = Blueprint('main', __name__)

USUARIO_CORRETO = os.getenv('USUARIO_ADMIN')
SENHA_CORRETA = os.getenv('SENHA_ADMIN')
TOKEN_ACESSO = os.getenv('TOKEN_ACESSO', 'acesso123')

cloudinary.config(
    cloud_name="kaikgarage",
    api_key="977435629795153",
    api_secret="eBwokPHQ9uz__XPUlVMTH5fwP1s"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/admin-entrada-secreta', methods=['GET', 'POST'])
def login():
    acesso = request.args.get('acesso')

    if request.method == 'GET' and acesso != TOKEN_ACESSO:
        return "Acesso negado", 403

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USUARIO_CORRETO and password == SENHA_CORRETA:
            session['usuario'] = username
            return redirect(url_for('main.adicionar_carro'))
        else:
            erro = 'Usuário ou senha inválidos'
            return render_template('login.html', error=erro)

    return render_template('login.html')

@main.route('/adicionar-carro', methods=['GET', 'POST'])
def adicionar_carro():
    if 'usuario' not in session:
        return redirect(url_for('main.login', acesso=TOKEN_ACESSO))

    if request.method == 'POST':
        nome = request.form.get('nome')
        valor = request.form.get('valor')
        cor = request.form.get('cor')
        descricao = request.form.get('descricao')
        ano = request.form.get('ano')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')

        try:
            valor = float(valor.replace('.', '').replace(',', '.'))
        except ValueError:
            flash("Valor inválido!", "danger")
            return redirect(url_for('main.adicionar_carro'))

        imagens = request.files.getlist('imagens')

        if not imagens or all(imagem.filename == '' for imagem in imagens):
            flash("Nenhuma imagem selecionada!", "danger")
            return redirect(url_for('main.adicionar_carro'))

        if not all(imagem.filename != '' and allowed_file(imagem.filename) for imagem in imagens):
            flash("Formato de arquivo inválido ou imagens vazias!", "danger")
            return redirect(url_for('main.adicionar_carro'))

        novo_carro = Carro(
            nome=nome,
            valor=valor,
            cor=cor,
            descricao=descricao,
            ano=int(ano),
            marca=marca,
            modelo=modelo
        )
        db.session.add(novo_carro)
        db.session.flush()  # pega o ID do carro antes de commitar

        try:
            for imagem in imagens:
                if imagem and allowed_file(imagem.filename):
                    upload_result = cloudinary.uploader.upload(imagem)
                    url_imagem = upload_result['secure_url']

                    imagem_carro = ImagemCarro(
                        url_imagem=url_imagem,
                        carro_id=novo_carro.id
                    )
                    db.session.add(imagem_carro)

            db.session.commit()
            flash("Carro cadastrado com sucesso!", "success")
            return redirect(url_for('main.carros_disponiveis'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar imagens: {str(e)}", "danger")
            return redirect(url_for('main.adicionar_carro'))

    carros = Carro.query.all()
    contagem = {}
    lista_exibicao = []

    for carro in carros:
        chave = f"{carro.nome} - {carro.cor}"
        contagem[chave] = contagem.get(chave, 0) + 1

    for chave, quantidade in contagem.items():
        lista_exibicao.append({"descricao": chave, "quantidade": quantidade})

    return render_template('adicionar_carro.html', lista_carros=lista_exibicao, carros=carros)

@main.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('main.login', acesso=TOKEN_ACESSO))

@main.route('/')
def home():
    carros = Carro.query.all()
    imagens = [imagem.url_imagem for carro in carros for imagem in carro.imagens]
    return render_template('index.html', imagens=imagens)

@main.route('/carros')
def carros_disponiveis():
    carros = Carro.query.all()
    return render_template('carros.html', carros=carros)

@main.route('/excluir_carro/<int:id>', methods=['POST'])
def excluir_carro(id):
    if 'usuario' not in session:
        return redirect(url_for('main.login', acesso=TOKEN_ACESSO))

    carro = Carro.query.get(id)
    if carro:
        try:
            for imagem in carro.imagens:
                db.session.delete(imagem)

            db.session.delete(carro)
            db.session.commit()
            flash("Carro excluído com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao excluir carro: {str(e)}", "danger")
    else:
        flash("Carro não encontrado!", "danger")

    return redirect(url_for('main.adicionar_carro'))

      


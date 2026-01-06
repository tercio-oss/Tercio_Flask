from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from estudo import db, bcrypt, app
from estudo.models import Contato, User, Post, PostComentario

import os
from werkzeug.utils import secure_filename


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar', validators=[DataRequired()])

    # Validação de E-Mail
    def validade_email(self, email):
        if User.query.filter(email=email.data).first():
            return ValidationError('Usuário já cadastrado com esse E-Mail!!!')
    

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8')) # Criptografar a senha
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )

        db.session.add(user)
        db.session.commit()
        
        return user


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar', validators=[DataRequired()])

    def login(self):
        # Recuperar o usuário do e-mail
        user = User.query.filter_by(email=self.email.data).first()

        # Verificar se a senha é válida
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                # Retorna o usuário
                return user
            else:
                raise Exception('Senha Incorreta!!!')
        else:
            raise Exception('Usuário não encontrado!!!')



class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar', validators=[DataRequired()])

    
    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            mensagem = self.mensagem.data,
            assunto = self.assunto.data
        )

        db.session.add(contato)
        db.session.commit()



class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar', validators=[DataRequired()])

    def save(self, user_id):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)
        post = Post(
            mensagem = self.mensagem.data,
            user_id = user_id,
            imagem = nome_seguro
        )

        caminho = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), # Pegar a pasta que está no nosso projecto
            app.config['UPLOAD_FILES'], # Definir a pasta que configuramos para o UPLOAD
            'post', # A pasta que está os Posts
            nome_seguro
        )

        imagem.save(caminho)
        db.session.add(post)
        db.session.commit()


class PostComentarioForm(FlaskForm):
    comentario = StringField('Comentário', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar', validators=[DataRequired()])


    def save(self, user_id, post_id):
        comentario = PostComentario(
            comentario = self.comentario.data,
            user_id = user_id,
            post_id = post_id
        )

        db.session.add(comentario)
        db.session.commit()
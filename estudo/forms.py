from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from estudo import db
from estudo.models import Contato


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

        
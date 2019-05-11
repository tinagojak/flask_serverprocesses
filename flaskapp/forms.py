from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class GetServerProcessesForm(FlaskForm):
	server = StringField('IP adresa Linux servera', 
						validators=[DataRequired()])
	username = StringField('Korisničko ime', 
						validators=[DataRequired()])
	password = PasswordField('Lozinka', 
						validators=[DataRequired()])
	submit = SubmitField('Dohvati procese')
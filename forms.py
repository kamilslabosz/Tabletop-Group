from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, SelectField, StringField, FieldList, FormField, TextAreaField, EmailField
from wtforms.validators import DataRequired


# Forms for Root Faction Assigner--------------------------------------------


class RootInfoForm(FlaskForm):
    players = SelectField("Number of players?", validators=[DataRequired()], choices=['2', '3', '4', '5', '6'])
    riverfolk = BooleanField("The Riverfolk expansion")
    underworld = BooleanField("The Underworld expansion")
    marauder = BooleanField("The Marauder expansion")
    cats = BooleanField("Marquise de Cat")
    birds = BooleanField("Eyrie Dynasties")
    woodland = BooleanField("Woodland Alliance")
    vagabond = BooleanField("Vagabond (both)")
    vagabond2 = BooleanField("2nd Vagabond")
    otters = BooleanField("Riverfolk Company")
    lizards = BooleanField("Lizard Cult")
    moles = BooleanField("Underground Duchy")
    crows = BooleanField("Corvid Conspiracy")
    badgers = BooleanField("Keepers in Iron")
    rats = BooleanField("Lord of the Hundreds")

    submit = SubmitField('Submit')


class DefaultPlayers(object):
    player1 = 'Player 1'
    player2 = 'Player 2'
    player3 = 'Player 3'
    player4 = 'Player 4'
    player5 = 'Player 5'
    player6 = 'Player 6'


class Root2PlayerForm(FlaskForm):
    player1 = StringField('Player 1')
    player2 = StringField('Player 2')
    submit = SubmitField('Submit')


class Root3PlayerForm(FlaskForm):
    player1 = StringField('Player 1')
    player2 = StringField('Player 2')
    player3 = StringField('Player 3')
    submit = SubmitField('Submit')


class Root4PlayerForm(FlaskForm):
    player1 = StringField('Player 1')
    player2 = StringField('Player 2')
    player3 = StringField('Player 3')
    player4 = StringField('Player 4')
    submit = SubmitField('Submit')


class Root5PlayerForm(FlaskForm):
    player1 = StringField('Player 1')
    player2 = StringField('Player 2')
    player3 = StringField('Player 3')
    player4 = StringField('Player 4')
    player5 = StringField('Player 5')
    submit = SubmitField('Submit')


class Root6PlayerForm(FlaskForm):
    player1 = StringField('Player 1')
    player2 = StringField('Player 2')
    player3 = StringField('Player 3')
    player4 = StringField('Player 4')
    player5 = StringField('Player 5')
    player6 = StringField('Player 6')
    submit = SubmitField('Submit')

# ------------------FORM FOR TO DO LIST ----------


class TodoForm(FlaskForm):
    todo_text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Submit')


# ----------CONTACT FORM------------------------

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

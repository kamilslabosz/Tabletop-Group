from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, SelectField, StringField, FieldList, FormField, TextAreaField, \
    EmailField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email, Length


# User Forms------------------------------------------------------------
class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired(), Length(min=4, max=10)])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class PasswordChangeForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat New Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")


# Forms for Root Faction Assigner--------------------------------------------


class RootInfoForm(FlaskForm):
    players = RadioField("Number of players?", choices=['2', '3', '4', '5', '6'], default='4')
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


# ----------CONTACT FORM------------------------

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


# --------------------------BOARD GAME COLLECTION FORMS--------------------------------


class BGGForm(FlaskForm):
    user = StringField('Your BoardGameGeek Username', validators=[DataRequired()])
    submit = SubmitField('Submit')


# --------------------------TTRPG CAMPAIGN TRACKER FORMS----------------------------


class AddCampaignForm(FlaskForm):
    name = StringField('Name of campaign', validators=[DataRequired()])
    game_system = StringField('Game system', validators=[DataRequired()])
    number_of_games = StringField('Number of sessions played', validators=[DataRequired()], default="0")
    exp_points = StringField('Number of experience collected', validators=[DataRequired()], default="0")
    gm_or_player = SelectField('Are you the GM or player?', validators=[DataRequired()],
                               choices=['Game Master', 'Player'])
    submit = SubmitField('Submit')


class EditCampaign(FlaskForm):
    pass


class AddSessionForm(FlaskForm):
    exp_points = StringField('Experience points earned', validators=[DataRequired()], default='0')
    submit = SubmitField('Submit')

import smtplib
import os
from functools import wraps

import sqlalchemy.exc
from flask import Flask, render_template, redirect, url_for, session, request, abort, flash
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from email.mime.text import MIMEText
from dotenv import load_dotenv

from forms import *
from scripts import root_available_factions, root_assign_faction, check_reach_vs_player_num, root_exclude_factions, \
    get_collection_from_bgg

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
Bootstrap(app)
Base = declarative_base()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///website.db')\
    .replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

load_dotenv()
my_email = os.environ.get('MY_EMAIL')
email_password = os.environ.get("MY_PASSWORD")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bg_association_table = db.Table('bg_association',
                                db.Column('user_id', ForeignKey('users.id'), primary_key=True),
                                db.Column('board_game_id', ForeignKey('board_games.id'), primary_key=True)
                                )

rpg_association_table = db.Table('rpg_association',
                                 db.Column('user_id', ForeignKey('users.id'), primary_key=True),
                                 db.Column('rpg_sessions_id', ForeignKey('rpg_sessions.id'), primary_key=True)
                                 )


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)
    games = db.relationship("BoardGame", secondary=bg_association_table, backref="owners")
    rpg_sessions = db.relationship("GameSession", secondary=rpg_association_table, backref="players")


class BoardGame(db.Model):
    __tablename__ = "board_games"
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(250), unique=True, nullable=False)


class GameSession(db.Model):
    __tablename__ = "rpg_sessions"
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(250), unique=True, nullable=False)
    game_system = db.Column(db.String(250), nullable=False)
    num_sessions = db.Column(db.Integer)


db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact-me", methods=["GET", "POST"])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        text_type = 'plain'
        with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=email_password)
            text = f"Name: {form.name.data}\nemail: {form.email.data}\n" \
                   f"\nMessage: {form.message.data}"
            msg = MIMEText(text, text_type, 'utf-8')
            msg['Subject'] = "New Message"
            msg['From'] = my_email
            msg['To'] = 'slaboszkamil@gmail.com'
            connection.sendmail(msg['From'], msg['To'], msg.as_string())

        return render_template('contact.html', sent=True, current_user=current_user)

    return render_template("contact.html", form=form, current_user=current_user)


# -------------------------------USERS---------------------------


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            flash("User with this email already exists")
            return redirect(url_for('login'))

        if form.password.data != form.password2.data:
            flash("Passwords don't match")
            return redirect(url_for('register'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Incorrect Password')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form, current_user=current_user)

# -----------------ROOT BOARDGAME--------------------------------


@app.route('/root', methods=["GET", "POST"])
def root_faction_assigner():
    form = RootInfoForm()
    session['factions'] = root_available_factions(riverfolk=form.riverfolk.data,
                                                  underworld=form.underworld.data,
                                                  marauder=form.marauder.data)
    if form.validate_on_submit():
        exclude_dict = {
            'Marquise de Cat': form.cats.data,
            'Eyrie Dynasties': form.birds.data,
            'Woodland Alliance': form.woodland.data,
            'Vagabond (both)': form.vagabond.data,
            '2nd Vagabond': form.vagabond2.data,
            'Riverfolk Company': form.otters.data,
            'Lizard Cult': form.lizards.data,
            'Underground Duchy': form.moles.data,
            'Corvid Conspiracy': form.crows.data,
            'Keepers in Iron': form.badgers.data,
            'Lord of the Hundreds': form.rats.data,
        }
        session['factions'] = root_exclude_factions(reach_dict=session.get('factions'),
                                                    factions_to_exclude=exclude_dict)
        players = form.players.data
        if int(players) > 4 and not form.riverfolk.data and not form.underworld.data and not form.marauder.data:
            flash("You need at least one expansion to play with 5+ players")
            return redirect(url_for('root_faction_assigner'))

        enough_reach = check_reach_vs_player_num(players=players, reach_dict=session.get('factions'))
        if not enough_reach:
            flash("Not enough reach among factions")
            return redirect(url_for('root_faction_assigner'))
        else:
            return redirect(url_for('root_players', players=players, current_user=current_user))
    return render_template('root.html', form=form, current_user=current_user)


@app.route('/root/<players>', methods=["GET", "POST"])
def root_players(players):
    print(session.get('factions'))
    if players == "2":
        default_players = DefaultPlayers()
        form = Root2PlayerForm(obj=default_players)
    elif players == "3":
        default_players = DefaultPlayers()
        form = Root3PlayerForm(obj=default_players)
    elif players == "4":
        default_players = DefaultPlayers()
        form = Root4PlayerForm(obj=default_players)
    elif players == "5":
        default_players = DefaultPlayers()
        form = Root5PlayerForm(obj=default_players)
    elif players == "6":
        default_players = DefaultPlayers()
        form = Root6PlayerForm(obj=default_players)

    if form.validate_on_submit():
        reach = session.get('factions')
        print(reach)
        players_list = []
        for index, field in enumerate(form):
            if index >= int(players):
                break
            else:
                players_list.append(field.data)
                print(players_list)

        players_dict = root_assign_faction(reach=reach, players=players_list)
        if not players_dict:
            return redirect(url_for('root_faction_assigner'))
        else:
            return render_template('root_players.html', players_dict=players_dict, current_user=current_user)
    return render_template('root_players.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# ----------------TO DO LIST-----------------------


@app.route("/todo", methods=["GET", "POST"])
def todo():

    if not session.get('enum_todo_dict'):
        session['enum_todo_dict'] = {}

    if request.method == "POST":
        try:
            session['todo_list'] += request.form['todo_text'].split(",")
        except KeyError:
            session['todo_list'] = request.form['todo_text'].split(",")

        enum_todo_list = enumerate(session.get('todo_list'))
        enum_todo_dict = session.get('enum_todo_dict')

        for item in enum_todo_list:
            try:
                enum_todo_dict[item] = request.form[f'btn-check-outlined{item[0]}']
            except KeyError:
                print('error')
                enum_todo_dict[item] = False

        session['enum_todo_dict'] = enum_todo_dict
        current_list = session.get('enum_todo_dict')
        print(current_list)
        return render_template('todo.html', tasks=current_list, current_user=current_user)
    current_list = session.get('enum_todo_dict')
    return render_template("todo.html",  tasks=current_list, current_user=current_user)


@app.route('/todo/clear', methods=["GET", "POST"])
def clear_todo_list():
    session['todo_list'] = []
    session['enum_todo_dict'] = {}
    return redirect(url_for('todo'))


# ----------TTRPG CAMPAIGN TRACKER-----------------------------
# TODO CREATE DATABASE OF USER GAMES AND ALLOW TO TRACK NUMBER OF SESSIONS
@app.route("/ttrpg")
def ttrpg_campaing_trakcer():
    page = "Tabletop RPG Campaign Tracker"
    return render_template("work_in_progress.html", target_page=page, current_user=current_user)


# ----------BOARDGAMES COLLECTION LIBRARY-----------------------------
# TODO CREATE DATABASE OF USER BOARDGAMES AND ALLOW BOARDGAMEGEEK COLLECTION IMPORT
@app.route("/boardgames", methods=["GET", "POST"])
def boardgames():
    if current_user.is_authenticated:
        form = BGGForm()
        if form.validate_on_submit():
            game_collection = get_collection_from_bgg(user=form.user.data)

            for game in game_collection:
                try:
                    edited_game = BoardGame.query.filter_by(link=game_collection[game]).first()
                    prev_owners = edited_game.owners
                    if current_user not in prev_owners:
                        edited_game.owners = prev_owners + [current_user]
                    else:
                        pass

                except AttributeError:
                    new_game = BoardGame(
                        game_name=game,
                        link=game_collection[game],
                        owners=[current_user],
                    )
                    db.session.add(new_game)

            db.session.commit()
            flash('Games added to collection')
            return render_template("bg_collection.html",
                                   form=form,
                                   game_collection=current_user.games,
                                   current_user=current_user)

        return render_template("bg_collection.html",
                               form=form,
                               game_collection=current_user.games,
                               current_user=current_user)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()


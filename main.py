import smtplib
import os

from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
from dotenv import load_dotenv


from forms import *
from scripts import root_available_factions, root_assign_faction, check_reach_vs_player_num, root_exclude_factions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
Bootstrap(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
load_dotenv()
my_email = os.environ.get('MY_EMAIL')
password = os.environ.get("MY_PASSWORD")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact-me", methods=["GET", "POST"])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        text_type = 'plain'
        with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            text = f"Name: {form.name.data}\nemail: {form.email.data}\n" \
                   f"\nMessage: {form.message.data}"
            msg = MIMEText(text, text_type, 'utf-8')
            msg['Subject'] = "New Message"
            msg['From'] = my_email
            msg['To'] = 'slaboszkamil@gmail.com'
            connection.sendmail(msg['From'], msg['To'], msg.as_string())

        return render_template('contact.html', sent=True)

    return render_template("contact.html", form=form)


# -----------------ROOT BOARDGAME--------------------------------

# TODO ALLOW TO EXCLUDE FACTIONS
@app.route('/root', methods=["GET", "POST"])
def root_faction_assigner():
    form = RootInfoForm()
    session['factions'] = root_available_factions(riverfolk=form.riverfolk.data,
                                                  underworld=form.underworld.data,
                                                  marauder=form.marauder.data)
    if form.validate_on_submit():
        players = form.players.data
        if int(players) > 4 and not form.riverfolk.data and not form.underworld.data and not form.marauder.data:
            return render_template('root.html', form=form, need_expansion=True)
        # check_reach_vs_player_num(players=players, reach_dict=session['factions'])
        return redirect(url_for('root_players', players=players))
    return render_template('root.html', form=form)


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
            return render_template('root_players.html', players_dict=players_dict)
    return render_template('root_players.html', form=form)


# ----------------TO DO LIST-----------------------
# TODO CHECKS COOKIES
@app.route("/todo", methods=["GET", "POST"])
def todo():
    form = TodoForm()
    if request.method == "POST":
        try:
            session['todo_list'] += form.todo_text.data.split(",")
        except KeyError:
            session['todo_list'] = form.todo_text.data.split(",")
        session['enum_todo_list'] = enumerate(session.get('todo_list'))
        current_list = session.get('enum_todo_list')
        print(current_list)
        form.todo_text.data = ""
        return render_template('todo.html', form=form, tasks=current_list)
    return render_template("todo.html", form=form)


@app.route('/todo/clear', methods=["GET", "POST"])
def clear_todo_list():
    session['todo_list'] = []
    return redirect(url_for('todo'))


# ----------TTRPG CAMPAIGN TRACKER-----------------------------
# TODO CREATE DATABASE OF USER GAMES AND ALLOW TO TRACK NUMBER OF SESSIONS
@app.route("/ttrpg")
def ttrpg_campaing_trakcer():
    page = "Tabletop RPG Campaign Tracker"
    return render_template("work_in_progress.html", target_page=page)


# ----------BOARDGAMES COLLECTION LIBRARY-----------------------------
# TODO CREATE DATABASE OF USER BOARDGAMES AND ALLOW BOARDGAMEGEEK COLLECTION IMPORT
@app.route("/boardgames")
def boardgames():
    page = "Boardgames Collection Library"
    return render_template("work_in_progress.html", target_page=page)


if __name__ == '__main__':
    app.run()


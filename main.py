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

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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
            return render_template('root.html', form=form, need_expansion=True)
        enough_reach = check_reach_vs_player_num(players=players, reach_dict=session.get('factions'))

        if not enough_reach:
            return render_template('root.html', form=form, need_reach=True)
        else:
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
        return render_template('todo.html', tasks=current_list)
    current_list = session.get('enum_todo_dict')
    return render_template("todo.html",  tasks=current_list)


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
    return render_template("work_in_progress.html", target_page=page)


# ----------BOARDGAMES COLLECTION LIBRARY-----------------------------
# TODO CREATE DATABASE OF USER BOARDGAMES AND ALLOW BOARDGAMEGEEK COLLECTION IMPORT
@app.route("/boardgames")
def boardgames():
    page = "Boardgames Collection Library"
    return render_template("work_in_progress.html", target_page=page)


if __name__ == '__main__':
    app.run()


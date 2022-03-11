from flask import Flask, render_template, redirect, url_for, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from forms import *
from scripts import root_available_factions, root_assign_faction

app = Flask(__name__)

app.config['SECRET_KEY'] = 'somestringfornow123a1!@asf2@!#$'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


# -----------------ROOT BOARDGAME--------------------------------


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
        players_list = []
        for index, field in enumerate(form):
            if index >= int(players):
                break
            else:
                players_list.append(field.data)
                print(players_list)

        players_dict = root_assign_faction(reach=reach, players=players_list)

        return render_template('root_players.html', players_dict=players_dict)
    return render_template('root_players.html', form=form)

# ----------------TO DO LIST-----------------------


@app.route("/todo", methods=["GET", "POST"])
def todo():
    form = TodoForm()
    if request.method == "POST":
        try:
            session['todo_list'] += form.todo_text.data.split(" ")
        except KeyError:
            session['todo_list'] = form.todo_text.data.split(" ")
        current_list = session.get('todo_list')
        print(current_list)
        form.todo_text.data = ""
        return render_template('todo.html', form=form, tasks=current_list)
    return render_template("todo.html", form=form)


@app.route('/todo/clear', methods=["GET", "POST"])
def clear_todo_list():
    session['todo_list'] = []
    return redirect(url_for('todo'))

if __name__ == '__main__':
    app.run(debug=True)

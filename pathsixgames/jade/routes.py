from flask import render_template, url_for
from pathsixgames.jade import jade

@jade.route('/')
def index():
    return render_template('jade/index.html')

@jade.route('/about')
def about():
    return render_template('jade/about.html')

@jade.route('/characters')
def characters():
    return render_template('jade/characters.html')

@jade.route('/book6')
def book6():
    return render_template('jade/adventureLog.html')

@jade.route('/book4')
def book4():
    return render_template('jade/adventureLog4.html')

@jade.route('/book5')
def book5():
    return render_template('jade/adventureLog5.html')

@jade.route('/rules')
def rules():
    return render_template('jade/rules.html')
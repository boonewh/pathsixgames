from flask import render_template, url_for
from pathsixgames.shackles import shackles

@shackles.route('/')
def index():
    return render_template('shackles/index.html')

@shackles.route('/book6')
def adventure_log():
    return render_template('shackles/adventure_log.html')

@shackles.route('/book1')
def book1():
    return render_template('shackles/adventure_log1.html')

@shackles.route('/book2')
def book2():
    return render_template('shackles/adventure_log2.html')

@shackles.route('/book3')
def book3():
    return render_template('shackles/adventure_log3.html')

@shackles.route('/book4')
def book4():
    return render_template('shackles/adventure_log4.html')

@shackles.route('/book5')
def book5():
    return render_template('shackles/adventure_log5.html')

@shackles.route('/dice')
def dice():
    return render_template('shackles/dice.html')

@shackles.route('/rules')
def rules():
    return render_template('shackles/rules.html')
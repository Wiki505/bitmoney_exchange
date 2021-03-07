from os import urandom
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, request, flash, url_for, session
from mysql.connector.errors import IntegrityError
from app.database_engine.mysql_engine import bitex_db, bitnet_db
from app.core.hash_engine import hash_string, network_hash_engine
from datetime import datetime
from uuid import uuid4
from app.core.BME import bitmoney_exchange_engine
from app.utils import email_engine
from app.utils.terminal_alert import alerts
bitmoney_platform = Flask(__name__)
# bootstrap = Bootstrap()
# bitmoney_platform.config['SECRET_KEY'] = urandom(12)

@bitmoney_platform.route('/')
def index():
    return redirect('http://0.0.0.0:1080/register')

@bitmoney_platform.route('/profile')
def profile():
    if 'username' in session:
        login_session = session['username']
        print(type(login_session))
        bitmoney_network_balance = bitnet_db().read(
            'SELECT SUM(amount) as total FROM bitmoney WHERE username="{username_session}" and status="0" UNION '
            'SELECT SUM(amount) as total FROM bitmoney_gold WHERE username="{username_session}" and status="0"'.format(username_session=login_session))
        print(bitmoney_network_balance)
        return render_template('account/home.html', balance=bitmoney_network_balance, username=login_session)
    else:
        flash('Inicia sesion para esta operacion!')
        return redirect(url_for('login'))


@bitmoney_platform.route('/bitmoney_transferring')
def bitmoney_tranfering():
    if 'username' in session:
        seed = session['username']
        if request.method == 'POST':
            root = request.form['seed_address']
            bitmoney_amount = request.form['bitmoney_amount']
            transfer_status = bitmoney_exchange_engine(seed, root, bitmoney_amount)
            if transfer_status == True:
                flash('{} fue tranferido con éxito a {}'.format(bitmoney_amount, root))
                return redirect(url_for('profile'))
            else:
                print(alerts.bad, 'Inclucion de metodo incorrecto!', request.method)
                flash('Existe un problema con tu cuenta prix!')
                return redirect(url_for('profile'))
        else:
            print(alerts.bad, 'Inclucion de metodo incorrecto!', request.method)
            flash('Existe un problema con tu cuenta prix!')
            return redirect(url_for('profile'))
    else:
        flash('Inicia sesion para esta operacion!')
        return redirect(url_for('login'))

@bitmoney_platform.route('/login')
def login():
    return render_template('account/login.html')

@bitmoney_platform.route('/login_action', methods=['POST'])
def login_action():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_string(request.form['password'])
        a = bitex_db().read("SELECT password FROM bm_users WHERE username='{}'".format(username))
        if a == []:
            flash('no existe')
            return redirect(url_for('login'))
        elif a[0][0] == password:
            print(a[0][0])
            session['username'] = username
            flash('simon')
            return redirect(url_for('home'))
        else:
            print(a)
            flash(a)
            return redirect(url_for('page_not_found'))
    else:
        print(alerts.bad, 'Inclucion de metodo incorrecto!', request.method)
        flash('Existe un problema con tu cuenta prix!')
        return redirect(url_for('profile'))

@bitmoney_platform.route('/register')
def register():
    return render_template('account/register.html')

@bitmoney_platform.route('/register_action', methods=['POST'])
def register_action():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_string(request.form['password'])
        try:
            mysql_control('bitmoney_exchange').write("INSERT INTO bm_users(username, email, password) VALUES ('{}','{}','{}')".format(username,email,password))

            flash('todo tuani prix!')
            return redirect(url_for('login'))
        except IntegrityError as err:
            print(err)
            flash('ya existe el chamaco')
            return redirect(url_for('register'))

@bitmoney_platform.route('/bitmoney_money')
def digital_money():
    return render_template('digital_money.html')

@bitmoney_platform.route('/bitmoney_action', methods=['POST'])
def digital_money_action():

    if request.method == 'POST':
        bmd = {
            'timestamp': str(datetime.now()),
            'username': request.form['username'],
            'amount': request.form['amount'],
            'difficulty': 1,
            'nonce': str(uuid4())
            }
        print(bmd)

        #   Hash and proof of work from Bitmoney Data
        hash_data = network_hash_engine(1, bmd).start_engine()

        mysql_control('bitmoney_network').write("INSERT INTO bitokens(hash_id, proof_of_work, difficulty, amount, nonce, username, timestamp) "
        "VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(hash_data[1], hash_data[0], bmd['difficulty'], bmd['amount'], bmd['nonce'], bmd['username'], bmd['timestamp']))

        flash('Dinero Digital agregado')
        return redirect(url_for('digital_money'))

@bitmoney_platform.route('/digital_money_process', methods=['POST'])
def digital_money_process():
    username = request.form['username']
    amount = request.form['amount']


@bitmoney_platform.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')

@bitmoney_platform.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html')



if __name__ == "__main__":
    bitmoney_platform.secret_key = urandom(12)
    bitmoney_platform.run(debug=True, host='0.0.0.0', port=1080)
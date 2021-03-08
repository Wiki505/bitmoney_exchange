from os import urandom
from flask import Flask, render_template, redirect, request, flash, url_for, session
from mysql.connector.errors import IntegrityError
from app.database_engine.mysql_engine import bitex_db, bitnet_db
from app.core.hash_engine import hash_string, network_hash_engine
from datetime import datetime
from hashlib import sha3_512
from uuid import uuid4
from app.core.BME import bitmoney_exchange_engine
from app.utils import email_engine
from app.utils.terminal_alert import alerts
bitmoney_platform = Flask(__name__)
# bootstrap = Bootstrap()
# bitmoney_platform.config['SECRET_KEY'] = urandom(12)

@bitmoney_platform.route('/')
def index():
    return redirect('http://0.0.0.0:1080/login')

@bitmoney_platform.route('/profile')
def profile():
    if 'username' in session:
        login_session = session['username']
        bitmoney = bitnet_db().read('SELECT SUM(amount) as total FROM bitmoney WHERE seed_address="{username_session}" and bitmoney_status="0"'.format(username_session=login_session))[0][0]
        if bitmoney == None:
            bitmoney = 0.0
        bitmoney_gold = bitnet_db().read('SELECT SUM(amount) as total FROM bitmoney_gold WHERE seed_address="{username_session}" and bitmoney_status="0"'.format(username_session=login_session))[0][0]
        if bitmoney_gold == None:
            bitmoney_gold = 0.0
        return render_template('account/profile.html', bm_balance=round(bitmoney, 2), bmg_balance=round(bitmoney_gold, 2), username=login_session)
    else:
        flash('Inicia sesion para esta operacion!')
        return redirect(url_for('login'))


@bitmoney_platform.route('/bitmoney_tranx', methods=['POST'])
def bitmoney_tranx():
    if 'username' in session:
        seed_address = session['username']
        if request.method == 'POST':
            root_address = request.form['root_address']
            bitmoney_amount = float(request.form['bitmoney_amount'])
            transfer_status = bitmoney_exchange_engine(seed_address, root_address, bitmoney_amount).start_transaction()
            print(transfer_status, "transfer status")
            if transfer_status == True:
                flash('{} fue tranferido con éxito a {}'.format(bitmoney_amount, root_address))
                return redirect(url_for('profile'))
            else:
                print(alerts.bad, 'error con la transferencia!')
                flash('Existe un problema con tu cuenta prix!')
                return redirect(url_for('profile'))
        else:
            print(alerts.bad, 'Inclucion ddddddddde metodo incorrecto!', request.method)
            flash('Existe un problema con tu cuenta prix!')
            return redirect(url_for('profile'))
    else:
        flash('Inicia sesion para esta operacion!')
        return redirect(url_for('login'))

@bitmoney_platform.route('/login')
def login():
    return render_template('account/login.html')

@bitmoney_platform.route('/init_session', methods=['POST'])
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
            return redirect(url_for('profile'))
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
            bitex_db().write("INSERT INTO bm_users(username, email, password) VALUES ('{}','{}','{}')".format(username,email,password))

            flash('todo tuani prix!')
            return redirect(url_for('login'))
        except IntegrityError as err:
            print(err)
            flash('ya existe el chamaco')
            return redirect(url_for('register'))

@bitmoney_platform.route('/new_bitmoney')
def new_bitmoney():
    return render_template('new_bitmoney.html')

@bitmoney_platform.route('/bitmoney_creation', methods=['POST'])
def bitmoney_creation():

    if request.method == 'POST':
        username = request.form['username']
        amount = request.form['amount']
        virtual_value = {
            'timestamp': datetime.now(),
            'amount': amount,
            'nonce': str(uuid4()),
            'seed': username,
        }
        #   New virtual value encryption
        hash_id = sha3_512(str(virtual_value).encode('utf-8')).hexdigest()

        #   Loading new virtual value on database
        bitnet_db().write("INSERT INTO bitmoney(hash_id, amount, nonce, seed_address, timestamp_input) "
                          "VALUES ('{}','{}','{}','{}','{}')".format(hash_id, virtual_value['amount'],
                                                                     virtual_value['nonce'], virtual_value['seed'],
                                                                     virtual_value['timestamp']))
        flash('Dinero Digital agregado')
        return redirect(url_for('new_bitmoney'))

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
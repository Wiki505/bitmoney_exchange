from app.database_engine.mysql_query import bitmoney_account_balance, bitmoney_gold_account_balance
from flask import Flask, render_template, redirect, request, flash, url_for, session
from app.database_engine.mysql_engine import run_database
from mysql.connector.errors import IntegrityError
from app.core.BME import bitmoney_exchange_engine
from app.core.hash_engine import hash_string
from app.core.bitmoney_generator import virtual_value_generator
from app.utils.terminal_alert import alerts
from os import urandom

bitmoney_platform = Flask(__name__)


# bootstrap = Bootstrap()
# bitmoney_platform.config['SECRET_KEY'] = urandom(12)

@bitmoney_platform.route('/')
def index():
    return 'TEST OK'


@bitmoney_platform.route('/profile')
def profile():
    if 'username' in session:
        login_session = session['username']
        bitmoney = run_database().read(bitmoney_account_balance.format(login_session))[0][0]
        if bitmoney == None:
            bitmoney = 0.0
        bitmoney_gold = run_database().read(bitmoney_gold_account_balance.format(login_session))[0][0]
        if bitmoney_gold == None:
            bitmoney_gold = 0.0
        return render_template('account/profile.html', bm_balance=round(bitmoney, 2),
                               bmg_balance=round(bitmoney_gold, 2), username=login_session)
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
                print(alerts.bad, 'error con la !')
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
        a = run_database().read("SELECT password FROM bitmoney_accounts WHERE username='{}'".format(username))
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
            run_database().write("INSERT INTO bm_users(username, email, password) VALUES ('{}','{}','{}')".format(username, email, password))

            flash('todo tuani prix!')
            return redirect(url_for('login'))
        except IntegrityError as err:
            print(err)
            flash('ya existe el chamaco')
            return redirect(url_for('register'))


@bitmoney_platform.route('/dashboard')
def dashboard():
    pass
    # return render_template('admin/darshboard.html')




@bitmoney_platform.route('/new_bitmoney')
def new_bitmoney():
    return render_template('new_bitmoney.html')


@bitmoney_platform.route('/create_bitmoney', methods=['POST'])
def bitmoney_creation():
    if request.method == 'POST':
        seed_address = request.form['seed_address']
        bitmoney_amount = request.form['bitmoney_amount']
        result = virtual_value_generator(seed_address, bitmoney_amount)
        if result == True:
            flash('Dinero Digital agregado')
            return redirect(url_for('new_bitmoney'))
        else:
            flash('Error prix, algun truquito salio mal')
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

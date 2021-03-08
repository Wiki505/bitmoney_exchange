from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer
from app.database_engine.mysql_engine import run_database
from itsdangerous.exc import BadSignature
import app

url_serializer = URLSafeSerializer("889782a5e0491ad44501ef37ef84ff98b5526c7a251d9075eea63c4daeaf662a")  # "compass"


def email_confirmation(server, email, id_string):
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_SSL": True,
        "MAIL_USE_TSL": False,
        "MAIL_USERNAME": 'bemburnmachine@gmail.com',
        "MAIL_PASSWORD": 'PTUEyS9hkucuRyj'}
    server.config.update(mail_settings)

    mail = Mail()
    mail.init_app(server)
    server_mail = Mail(server)

    url_validation = url_serializer.dumps([email, str(id_string)])

    msg = Message("Verificación de Cuenta",
                  sender=("Bitmoney Exchange", "exchangebitmoney@gmail.com"),
                  recipients=["%s" % email],
                  body="""
                  Gracias por utilizar los servicios de BitMoney Exchange, has click en el enlace para validar tu cuenta.
                  ---> http://0.0.0.0:1080/account_validation/%s

                  Para mayor información: +505 7608 7171 | @gmail.com
                  """ % url_validation)
    server_mail.send(msg)


def email_validation(token):
    try:
        data = url_serializer.loads(token)
        email = data[0]
        username = data[1]
    except BadSignature as err:
        print(err)
        return False

    db_data = run_database.read(
        "SELECT email, username FROM bm_users WHERE email='{}' AND USER_ID='{}'".format(email, username))
    if email == db_data[0][0] and username == db_data[0][1]:
        bitex_db().write("UPDATE bm_users SET account_status='{}' WHERE email='{}' AND USER_ID='%s'".format(1, email, username))
        return True
    else:
        return False
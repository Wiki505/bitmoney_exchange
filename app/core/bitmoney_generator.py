from app.database_engine.mysql_query import bitmoney_generator
from app.database_engine.mysql_engine import run_database
from app.utils.terminal_alert import alerts
from datetime import datetime
from hashlib import sha3_512
from uuid import uuid4, UUID
import pickle


def virtual_value_generator(seed_address, bitmoney_amount, tranx_nonce=None):
    bitmoney_value_data = {
        'tranx_nonce': str(uuid4()),
        'bitmoney_amount': bitmoney_amount,
        'seed_address': seed_address,
        'seed_type': 0,
        'timestamp': str(datetime.now())
    }

    if tranx_nonce != None:
        try:
            bitmoney_value_data['tranx_nonce'] = str(UUID(tranx_nonce))
            bitmoney_value_data['seed_type'] = 1

        except(AttributeError, ValueError) as err:
            print(alerts.bad, 'not a valid uuid string', err)
            return False

    hash_id = sha3_512(pickle.dumps(bitmoney_value_data)).hexdigest()

    run_database().write(bitmoney_generator.format(bitmoney_value_data['seed_address'], hash_id, bitmoney_value_data['bitmoney_amount'],
                         bitmoney_value_data['tranx_nonce'], bitmoney_value_data['seed_address'],bitmoney_value_data['timestamp']))

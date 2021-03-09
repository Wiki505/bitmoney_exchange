from app.database_engine.mysql_query import bitmoney_generator
from app.database_engine.mysql_engine import run_database
from app.utils.terminal_alert import alerts
from datetime import datetime
from hashlib import sha3_512
from uuid import uuid4, UUID
import pickle

def bitmoney_value(seed_addr, bitmoney_amount, tranx_nonce=None):

    bitmoney_value_data = {
        'tranx_nonce':str(uuid4()),
        'bitmoney_amount':bitmoney_amount,
        'seed_address':seed_addr,
        'tranx_return':False,
        'timestamp':str(datetime.now())
        }

    if tranx_nonce != None:
        try:
            bitmoney_value_data['tranx_nonce'] = str(UUID(tranx_nonce))
            bitmoney_value_data['tranx_return'] = True

        except(AttributeError, ValueError) as err:
            print(alerts.bad, err)
            return False
    else:
        pass

    hash_id = sha3_512(pickle.dumps((bitmoney_value_data))).hexdigest()
    # for i in bitmoney_value_data:
    #     print(i, bitmoney_value_data[i])
    run_database().write(bitmoney_generator.format(hash_id, bitmoney_value_data['bitmoney_amount'], bitmoney_value_data['nonce'], bitmoney_value_data['timestamp']))



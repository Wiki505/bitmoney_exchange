from hashlib import sha3_512
from pickle import dumps
from uuid import uuid4
from datetime import datetime
from app.utils.terminal_alert import alerts
from app.database_engine.mysql_engine import bitex_db, bitnet_db
from app.settings import bitmoney_exchange_settings
from app.core.hash_engine import network_hash_engine

digital_money_id = '715fbc5475a55d9094d397b585a429c03b2f02668eb2f28a744d5b2680c2873408864e34c08be26fceac8deb9ee25172150cce9b2e045919f665275e4f9f8f93'

class bitmoney_exchange_engine():
    def __init__(self, seed_address, root_address, tranx_amount):
        self.__transaction_fees = round(tranx_amount * bitmoney_exchange_settings['TRANSACTION_FEES'], 2)
        self.__network_tranx = round(tranx_amount + self.__transaction_fees, 2) # Total transaction, fees included
        self.__timestamp = datetime.now()
        self.__nonce = str(uuid4())
        self.__seed_balance = None
        self.__seed = seed_address
        self.__root = root_address

    def exchange_engine(self):
        account_status = bitnet_db().read('SELECT hash_id, amount FROM bitmoney WHERE username="{0}" '
                                          'and bitmoney_status="0" ORDER BY amount DESC'.format(self.__seed))

        print(self.__network_tranx)
        bitpi = len(account_status)  # BitMoney Pieces, all values with True status.
        address_balance = 0
        counter = 0
        for bitmoney_data in account_status:
            counter += 1
            address_balance += bitmoney_data[1]

            if address_balance < self.__network_tranx:
                pass
            elif address_balance >= self.__network_tranx:
                bitmoney_return = round(address_balance - self.__network_tranx, 2)
                print('Bitmoney de Retorno', bitmoney_return)
                print(address_balance, '----',self.__network_tranx)
                hash_id = network_hash_engine((bitmoney_return, self.__nonce, self.__timestamp)).start_engine()
                print(hash_id, self.__nonce, self.__timestamp)
                return hash_id, self.__nonce, self.__timestamp
            else:
                continue
            if counter == bitpi:
                print('Need more Funds!')
                break

    def network_address_check(self):
        address_status = bitex_db().read("""SELECT EXISTS(SELECT account_status from bm_users WHERE username='{0}') UNION
        SELECT EXISTS(SELECT account_status from bm_users WHERE username='{1}')""".format(self.__seed, self.__root))

        if len(address_status) == 2 or address_status[0][0] == False:
            print(alerts.bad, 'Invalid account')
            return False
        elif len(address_status) == 1 and address_status[0][0] == True:
            print(alerts.good, 'Accounts are OK')
            return True

    def seed_account_balance(self):
        balance = round(bitnet_db().read('SELECT SUM(amount) as total FROM bitmoney WHERE username="{0}" and bitmoney_status="0"'.format(self.__seed))[0][0], 2)
        print(alerts.bad, alerts.good, balance)
        if balance == None:
            return False
        elif balance >= self.__network_tranx:
            self.__seed_balance = balance
            return True
        elif balance < self.__network_tranx:
            self.__seed_balance = balance
            return False

    def bitmoney_transaction(self):
        if self.network_address_check() == True:
            print(alerts.good, 'Address Cheked')
            if self.seed_account_balance() == True:
                print(alerts.good, 'Address has sufficient funds!')
                self.exchange_engine()
                print(alerts.excellent, 'The transaction was successful')
            else:
                print(alerts.warning, 'Address does not have sufficient funds')
                print(alerts.warning, self.__seed_balance, self.__network_tranx)
                print(alerts.warning, 'Address Balance: {} | Funds needed: {}'.format(self.__seed_balance, str((self.__network_tranx - self.__seed_balance))))
        else:
            print(alerts.bad, 'Address invalid!')
            return False

a = bitmoney_exchange_engine('canino', 'perrito', 97.1).bitmoney_transaction()










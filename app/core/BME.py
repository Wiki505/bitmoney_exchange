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

    def btmoney_miner_gold(self):
        pass

    def new_virtual_value(self, assigned_to, amount):
            #   root data for new virtual value
            virtual_value = {
                'amount': amount,
                'timestamp':self.__timestamp,
                'nonce':self.__nonce,
                'seed': assigned_to,
                }
            #   New virtual value encryption
            hash_id = sha3_512(str(virtual_value).encode('utf-8')).hexdigest()

            #   Loading new virtual value on database
            bitnet_db().read("INSERT INTO bitmoney(hash_id, amount, nonce, seed_address, timestamp_in) "
                             "VALUES ('{}','{}','{}','{}')".format(hash_id, virtual_value['amount'], virtual_value['nonce'], virtual_value['seed'], virtual_value['timestamp']))
            return True

    def previous_hash_id(self):
        root_hash = bitnet_db().read("SELECT tranx_hash_id FROM bitmoney_ledger ORDER BY id DESC LIMIT 1")[0][0]
        print(alerts.good, 'Previous Hash: {}'.format(root_hash))
        return root_hash

    def __tranx_run(self):
        # Previous transaction hash for chain the new transaction
        previous_hash = self.previous_hash_id()
        tranx_data = {
            'seed_address': self.__seed,
            'root_address': self.__root,
            'tranx_amount': self.__network_tranx,
            'tranx_fees': self.__transaction_fees,
            'tranx_nonce': self.__nonce,
            'timestamp': self.__timestamp,
            'previous_hash': previous_hash,
            'bitmoney_gold_mined': 0,
            }

        #   data encryption from new transaction
        hash_data_result = network_hash_engine(tranx_data).start_engine()

        #   bitmoney_gold mined from transaction
        bitmoney_gold_mined = 0

        #   Loading all transaction data in bitmoney ledger
        x = bitnet_db().write(
            "INSERT INTO bitmoney_ledger(seed_address, root_address, tranx_amount, tranx_fees, proof_of_work, tranx_hash_id, tranx_nonce, timestamp, bitmoney_gold_mined) "
            "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(self.__seed, self.__root, self.__network_tranx,
                                                                      self.__transaction_fees,
                                                                      hash_data_result[0], hash_data_result[1],
                                                                      self.__nonce, self.__timestamp,
                                                                      bitmoney_gold_mined))

    @property
    def exchange_engine(self):
        account_status = bitnet_db().read('SELECT hash_id, amount FROM bitmoney WHERE username="{0}" '
                                          'and bitmoney_status="0" ORDER BY amount DESC'.format(self.__seed))

        bitpi = len(account_status)  # BitMoney Pieces, all values with True status.
        address_balance = 0
        counter = 0

        for bitmoney_data in account_status:
            counter += 1
            address_balance += bitmoney_data[1]

            if address_balance < self.__network_tranx:
                pass
            elif address_balance > self.__network_tranx:
                bitmoney_return = round(address_balance - self.__network_tranx, 2)
                # Insertando el saldo por piezas y creando una nueva pieza por cambio
                self.new_virtual_value(self.__root, bitmoney_return)
                self.__tranx_run()
                return True
            elif address_balance == self.__network_tranx:
                self.__tranx_run()
                return True
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
                # self.exchange_engine
                print(alerts.excellent, 'The transaction was successful')
            else:
                print(alerts.warning, 'Address does not have sufficient funds')
                print(alerts.warning, self.__seed_balance, self.__network_tranx)
                print(alerts.warning, 'Address Balance: {} | Funds needed: {:.2f}'.format(self.__seed_balance, (self.__network_tranx - self.__seed_balance)))
        else:
            print(alerts.bad, 'Address invalid!')
            return False






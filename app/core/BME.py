from hashlib import sha3_512
from pickle import dumps
from uuid import uuid4
from datetime import datetime
from app.utils.terminal_alert import alerts
from app.database_engine.mysql_engine import run_database
from app.database_engine.mysql_query import cheking_address, previous_tranx_hash, updating_status
from app.settings import bitmoney_exchange_settings
from app.core.bitmoney_generator import bitmoney_value_generator
from app.core.hash_engine import network_hash_engine
from json import dumps
digital_money_id = '715fbc5475a55d9094d397b585a429c03b2f02668eb2f28a744d5b2680c2873408864e34c08be26fceac8deb9ee25172150cce9b2e045919f665275e4f9f8f93'


class bitmoney_exchange_engine():
    def __init__(self, seed_address, root_address, tranx_amount):
        self.tranx_amount = tranx_amount
        self.tranx_fees = round(tranx_amount * bitmoney_exchange_settings['TRANSACTION_FEES'], 2)
        self.total_tranx = round(tranx_amount + self.tranx_fees, 2)  # Total transaction, fees included
        self.timestamp = datetime.now()
        self.nonce = str(uuid4())
        # variables de intercambio
        self.seed = seed_address
        self.root = root_address
        self.seed_balance = None
        self.bitmoney_inputs = {}


    def check_accounts_status(self):
        accounts_status = run_database().read(cheking_address.format(self.seed, self.root))
        if len(accounts_status) == 2 or accounts_status[0][0] == False:
            print(alerts.bad, 'Invalid account')
            return False
        elif len(accounts_status) == 1 and accounts_status[0][0] == True:
            print(alerts.good, 'Accounts are OK')
            return True


    def previous_tranx_hash(self):
        root_hash = run_database().read(previous_tranx_hash)[0][0]
        print(alerts.good, 'Previous Hash: {}'.format(root_hash))
        return root_hash


    def updating_bitmoney_status_spend(self):
        for bitmoney in self.bitmoney_inputs:
            run_database().write(updating_status.format(self.timestamp, self.seed, bitmoney))


    def account_balance(self):
        balance = run_database().read('SELECT SUM(amount) as total FROM bitmoney WHERE seed_address="{0}" and bitmoney_status="0"'.format(self.seed))[0][0]
        print(alerts.bad, alerts.good, balance)
        if balance == None:
            return False
        elif balance >= self.total_tranx:
            self.__seed_balance = balance
            return True
        elif balance < self.total_tranx:
            self.__seed_balance = balance
            return False

    def process_tranx(self):
        # Previous transaction hash for chain the new transaction
        previous_hash = self.previous_tranx_hash()
        tranx_data = {
            'seed_address': self.seed,
            'root_address': self.root,
            'tranx_amount': self.tranx_amount,
            'tranx_fees': self.tranx_fees,
            'tranx_nonce': self.nonce,
            'timestamp': self.timestamp,
            'previous_hash': previous_hash,
            'bitmoney_gold_mined': 0,
            'bitmoney_inputs': self.bitmoney_inputs,
        }

        #   data encryption from new transaction
        hash_data_result = network_hash_engine(tranx_data).start_engine()
        # print(self.__seed, self.__root, self.__tranx_amount, self.__tranx_fees, hash_data_result[0], hash_data_result[1], previous_hash, self.__bitmoney_inputs, self.__nonce, self.__timestamp)
        #   bitmoney_gold mined from transaction
        bitmoney_gold_mined = 0
        #
        # bitmoney_value_generator(self.seed, self.tranx_amount, tranx_nonce=self.nonce)
        # #   Transfering fees per transferring to the network
        # bitmoney_value_generator('BME', self.tranx_fees, tranx_nonce=self.nonce)
        #

        print(self.seed, self.root, self.tranx_amount, self.tranx_fees, hash_data_result[0], self.nonce, hash_data_result[1], previous_hash, self.bitmoney_inputs, self.timestamp, bitmoney_gold_mined)


        # #   Loading all transaction data in bitmoney ledger
        run_database().write("INSERT INTO bitmoney_ledger(seed_address, root_address, tranx_amount, tranx_fees, proof_of_work, tranx_nonce, tranx_hash_id, previous_hash, inputs, timestamp, bitmoney_gold_mined) "
                             "VALUES  ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.seed, self.root, self.tranx_amount, self.tranx_fees, hash_data_result[0], self.nonce,
                                                                                                       hash_data_result[1], previous_hash, dumps(self.bitmoney_inputs), self.timestamp, bitmoney_gold_mined))
        return True

    # @property
    def bitmoney_collector(self):
        bitmoney_values = run_database().read('SELECT hash_id, amount FROM bitmoney WHERE seed_address="{0}" '
                                             'and bitmoney_status="0" ORDER BY amount DESC'.format(self.seed))

        bitpi = len(bitmoney_values)  #  BitMoney Pieces, all values with No Spend status.
        account_balance = 0 #   Total balance in account
        counter = 0 #   Bucle laps, at the end always be equal to bitpi

        for bitmoney_data in bitmoney_values:
            #   se agrega cada valor virtual a la suma transaccional
            self.bitmoney_inputs[bitmoney_data[0]] = bitmoney_data[1]
            #   se cuenta cada pieza de valor
            counter += 1
            #   se suma el valor de cada pieza al balance general de la cuenta
            account_balance += bitmoney_data[1]
            #   si el balance general es menor al total de la transaccion, pasa para sumar otra pieza
            if account_balance < self.total_tranx:
                pass
            #   si el balance general es mayor al total de la transaccion, procesar transaccion,
            #   agregar Nonce de la transaccion al bitmoney de retorno
            elif account_balance > self.total_tranx:

                #   updating bitmoney pieces to spend!
                self.updating_bitmoney_status_spend()
                #   se calcula el monto de retorno
                bitmoney_return = round(account_balance - self.total_tranx, 2)
                #  creando una nueva pieza por retorno de la transaccion
                bitmoney_value_generator(self.seed, bitmoney_return, tranx_nonce=self.nonce)

                bitmoney_value_generator(self.root, self.tranx_amount, tranx_nonce=self.nonce)
                #   Transfering fees per transferring to the network
                bitmoney_value_generator('BME', self.tranx_fees, tranx_nonce=self.nonce)

                #   Loading all transaction data in bitmoney ledger
                #   processed the transaction
                self.process_tranx()

                return True
            #   si el balance general es igual al monto de la transaccion, procesar
            elif account_balance == self.total_tranx:
                #   procesando la transaccion
                #   updating bitmoney pieces to spend!
                self.updating_bitmoney_status_spend()
                #   Transferring the bitmoney to final user

                bitmoney_value_generator(self.root, self.tranx_amount, tranx_nonce=self.nonce)
                #   Transfering fees per transferring to the network
                bitmoney_value_generator('BME', self.tranx_fees, tranx_nonce=self.nonce)

                self.process_tranx()
                print(self.bitmoney_inputs)
                return True
            else:
                continue

            #   si el contador es igual a la cantidad de piezas,
            #   los fonsos son isuficientes, necesita recargar valores
            if counter == bitpi:
                print('Need more Funds!')
                break


    def start_transaction(self):
        if self.check_accounts_status() == True:
            print(alerts.good, 'Address Cheked')
            if self.account_balance() == True:
                print(alerts.good, 'Address has sufficient funds!')
                self.bitmoney_collector()
                print(alerts.excellent, 'The transaction was successful')
                return True
            else:
                print(alerts.warning, 'Address does not have sufficient funds')
                print(alerts.warning, self.seed_balance, self.total_tranx)
                print(alerts.warning, 'Address Balance: {} | Funds needed: {:.2f}'.format(self.__seed_balance, (self.total_tranx - self.__seed_balance)))
                return False
        else:
            print(alerts.bad, 'Address invalid!')
            return False

# bitmoney_exchange_engine('canino','perrito', 9).seed_account_balance()

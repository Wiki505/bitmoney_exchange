from hashlib import sha3_512
from pickle import dumps
from time import time
from app.utils.terminal_alert import alerts

class network_hash_engine():
    # el tiempo no lleva 'round' para capturar lo mas preciso
    # se redondea al resultado final
    start_time = time()

    def __init__(self, data):
        self.__difficulty = 3
        self.__data_serial = dumps(str(data).encode('utf-8'))
        self.__hash_string = sha3_512(self.__data_serial).hexdigest()

    # @check_authorization
    def start_engine(self):
        proof_of_work = 1
        while True:
            if self.__hash_string[:self.__difficulty] == ('0' * self.__difficulty):
                break
            else:
                proof_of_work += 1
                self.__hash_string = sha3_512(self.__hash_string.encode('utf-8')).hexdigest()
        print(alerts.good, 'Proof of Work: {:,.0f} | Hash String: {}'.format(proof_of_work, self.__hash_string))
        #   return proof of work and hash string
        end_time = time()
        total_time = end_time - self.start_time
        hash_per_second = round(proof_of_work / total_time, 2)
        print(alerts.good, 'Hash average: {:,.2f} Hashes'.format(hash_per_second))
        print(alerts.good, 'Time process engine: {} miliseconds!'.format(total_time))
        return (proof_of_work, self.__hash_string)

def hash_string(data):
    hash_object = sha3_512(str(data).encode('utf-8')).hexdigest()
    return hash_object


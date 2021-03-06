from app.database_engine.mysql_engine import mysql_control
from app.utils.terminal_alert import alerts

from app.core.hash_engine import network_hash_engine


def exchange_engine(seed_addr, tranx_amount):

    account_status = mysql_control('bitmoney_network').read('SELECT hash_id, amount FROM bitmoney WHERE username="{0}" and bitmoney_status="0" ORDER BY amount DESC'.format(seed_addr))
    print(account_status)
    bitpi = len(account_status) # BitMoney Pieces, all values with True status.
    address_balance = 0
    counter = 0
    for bitmoney_data in account_status:
        counter += 1
        address_balance += bitmoney_data[1]

        if address_balance < tranx_amount:
            pass
        elif address_balance >= tranx_amount:
            bitmoney_return = round(address_balance - tranx_amount, 2)
            print('Bitmoney de Retorno', bitmoney_return)
            print(address_balance, tranx_amount)
            hash_id = network_hash_engine(bitmoney_return).start_engine()
            return hash_id
        else:
            continue
        if counter == bitpi:
            print('Need more Funds!')
            break

        print(counter, address_balance, account_status)



exchange_engine('canino',100.01)



    # if amount > bitmoney_total:
    #     bitmoney_total = bitmoney_total + bitmoney_data[1]
    #     print(bitmoney_data)








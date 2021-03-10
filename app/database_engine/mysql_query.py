
#   bitmoney generator query "bm_generator"
bitmoney_generator = "INSERT INTO bitmoney(hash_id, amount, nonce, seed_address, timestamp_input) VALUES ('{}','{}','{}','{}','{}')"

#   Loading account balance on profile view - RUN.PY
bitmoney_account_balance = 'SELECT SUM(amount) as total FROM bitmoney WHERE seed_address="{}" and bitmoney_status="0"'
bitmoney_gold_account_balance = 'SELECT SUM(amount) as total FROM bitmoney_gold WHERE seed_address="{}" and bitmoney_status="0"'

# cheking the address status in the network, BME.PY
cheking_address = "SELECT EXISTS(SELECT account_status from bitmoney_accounts WHERE username='{}') UNION SELECT EXISTS(SELECT account_status from bitmoney_accounts WHERE username='{}')"

# Previous hash BME.PY
previous_tranx_hash = "SELECT tranx_hash_id FROM bitmoney_ledger ORDER BY id DESC LIMIT 1"

# Updating bitmoney status BME.PY
updating_status = "UPDATE bitmoney SET bitmoney_status='1', timestamp_output='{}' WHERE seed_address='{}' AND hash_id='{}'"




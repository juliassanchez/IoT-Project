'''Main project python file'''
import requests
from sqlalchemy import update, insert, delete
from sqltable import SQLTable
from gateway_outcome import gateway_outcome, disconnected_gateways
from dotenv import load_dotenv
import os
load_dotenv() # Load dotenv to use the token

def update_gateway(gateway_id):
    '''Method to update the gateway SQL table'''

    # Obtain the json file for a given gateway (by its id)
    http_string = 'https://eu1.cloud.thethings.network/api/v3/gs/gateways/' + gateway_id + '/connection/stats'
    r = requests.get(http_string, headers={'Authorization': 'Bearer ' + os.getenv('TOKEN_2')})
    json_gateway_file = r.json()

    if json_gateway_file.get('last_status_received_at') == None:
        # In case the gateway is completely disconnected
        last_status = '2000-01-01T00:00:00.000000000Z'
        gateway_ip = str(None)
    else:
        last_status = json_gateway_file['last_status_received_at']
        gateway_ip = json_gateway_file['gateway_remote_address']['ip']

    # Update the obtained information on the SQL Table
    sqltable = SQLTable()
    if sqltable.checkIfInserted(gateway_id) == None:
        stmt = insert(sqltable.gateway).values(gateway_id=gateway_id,
                                               last_status_received_at=last_status,
                                               ip=gateway_ip)
    else:
        stmt = update(sqltable.gateway).where(sqltable.gateway.c.gateway_id == gateway_id).values(last_status_received_at=last_status)
    #stmt = delete(sqltable.gateway)
    with sqltable.engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

def iterate(initial_table):
    '''Method to periodically iterate and update the gateway SQL Table'''
    # For each gateway we update its information with update_gateway()
    for gateway_id in initial_table:
        update_gateway(gateway_id)

gateway_id_table = ['agricola-punica','ripatransone','montecarotto','polito','monte-narcao', 'laird-lab']
iterate(gateway_id_table)

if __name__ == '__main__':
    #here we must iterate over the given table, with different ids for a period of time
    print(gateway_outcome())
    print(disconnected_gateways(1))



'''Main project python file'''
import requests
from sqlalchemy import update, insert, delete
from sqltable import SQLTable
from gateway_outcome import gateway_outcome
from dotenv import load_dotenv
import os

load_dotenv() # Load dotenv to use the token

def update_gateway(gateway_id):
    '''Method to update the gateway SQL table'''

    # Obtain the json file for a given gateway (by its id)
    http_string = 'https://eu1.cloud.thethings.network/api/v3/gs/gateways/' + gateway_id + '/connection/stats'
    r = requests.get(http_string, headers={'Authorization': 'Bearer ' + os.getenv('TOKEN')})
    json_gateway_file = r.json()

    try:
        # Update the obtained information on the SQL Table
        sqltable = SQLTable()
        if not sqltable.checkIfInserted(gateway_id):
            stmt = insert(sqltable.gateway).values(gateway_id=gateway_id,
                                                   last_status_received_at=json_gateway_file['last_status_received_at'],
                                                   ip=json_gateway_file['gateway_remote_address']['ip'])
        else:
            stmt = update(sqltable.gateway).values(gateway_id=gateway_id,
                                               last_status_received_at=json_gateway_file['last_status_received_at'],
                                               ip=json_gateway_file['gateway_remote_address']['ip'])
        #stmt = delete(sqltable.gateway)
        with sqltable.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    #If an error occurred when trying to read a value from the json file (key not found in the json)
    except Exception:
        return 'An unknown error occurred while trying to obtain the information from The Things Network'



def iterate(initial_table):
    '''Method to periodically iterate and update the gateway SQL Table'''
    # For each gateway we update its information with update_gateway()
    for gateway_id in initial_table:
        update_gateway(gateway_id)


if __name__ == '__main__':
    #here we must iterate over the given table, with different ids for a period of time
    print(update_gateway('laird-lab'))
    print(gateway_outcome())




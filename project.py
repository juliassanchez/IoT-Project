'''Main project python file'''
import os
import requests
from sqlalchemy import update, insert
from sqltable import SQLTable
from gateway_outcome import output
from dotenv import load_dotenv
from datetime import datetime
from dateutil import tz

load_dotenv() # Load dotenv to use the token
# Load statuses in cte instead of uct
to_zone= tz.gettz('Europe/Italy')
from_zone = tz.gettz('UTC')


def update_gateway(gateway_id):
    '''Method to update the gateway SQL table'''

    # Obtain the json file for a given gateway (by its id)
    http_string = 'https://eu1.cloud.thethings.network/api/v3/gs/gateways/' + gateway_id + '/connection/stats'
    r = requests.get(http_string, headers={'Authorization': 'Bearer ' + os.getenv('TOKEN')})
    json_gateway_file = r.json()

    if json_gateway_file.get('last_status_received_at') == None:
        # In case the gateway is completely disconnected
        last_status_cet = '2000-01-01 00:00:00' # Arbitrary date to disconnected gateways
        gateway_ip = str(None)
    else:
        last_status = json_gateway_file['last_status_received_at']
        last_status_cet = str(datetime.strptime(str(last_status)[:19],'%Y-%m-%dT%H:%M:%S').replace(tzinfo=from_zone).
                              astimezone(to_zone))[:19]
        gateway_ip = json_gateway_file['gateway_remote_address']['ip']

    # Update the obtained information on the SQL Table
    sqltable = SQLTable()
    if sqltable.checkIfInserted(gateway_id) == None:
        stmt = insert(sqltable.gateway).values(gateway_id=gateway_id,
                                               last_status_received_at= last_status_cet,
                                               ip=gateway_ip)
    else:
        stmt = update(sqltable.gateway).where(sqltable.gateway.c.gateway_id == gateway_id).values(
            last_status_received_at=last_status_cet)
    # Commit changes to database
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
    # Printing the outputs
    output(1)



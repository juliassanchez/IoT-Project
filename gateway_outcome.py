'''Python file for printing the gateway outcome'''
from datetime import datetime
from sqltable import SQLTable
from sqlalchemy import select
from tabulate import tabulate

def output(num_hours):
    sqltable = SQLTable()
    stmt = select('*').select_from(sqltable.gateway)
    result = sqltable.session.execute(stmt).fetchall()
    print(gateway_outcome(sqltable, result), '\n')
    print(disconnected_gateways(sqltable, result, num_hours))

def gateway_outcome(sqltable, result):
    '''Method to return the table containing the gateway outcome'''

    table = [[]]
    table.append(sqltable.gateway.columns)
    # Order by first disconnected
    print("------------------------------GATEWAYS STATUS------------------------------")
    for x in sorted(result, key=lambda row: row[1]): table.append(x)
    return tabulate(table, headers='firstrow', tablefmt='fancy_grid')

def disconnected_gateways(sqltable, result, num_hours):
    '''Method to show the gateways disconnected for num_hours hours'''
    now = datetime.now()
    table = []
    for i in range(len(result)):
        if result[i][1] != str(None):
            last_status_received = datetime.strptime(str(result[i][1]), '%Y-%m-%d %H:%M:%S') # 2023-06-12T08:49:18.394358877Z
        else:
            last_status_received = datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        diff_in_hours = (now - last_status_received).total_seconds() / 3600
        if diff_in_hours >= num_hours and last_status_received != 0:
            table.append(tuple((result[i])))

    ordered_table = [[]]
    ordered_table.append(sqltable.gateway.columns)
    # Order by first disconnected - not checked
    print("----------------GATEWAYS DISCONNECTED BY AT LEAST %i HOUR/S----------------"%num_hours)
    for x in sorted(table, key=lambda row: row[1]):
        ordered_table.append(x)

    return tabulate(ordered_table, headers='firstrow', tablefmt='fancy_grid')
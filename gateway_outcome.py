'''Python file for printing the gateway outcome'''
from sqltable import SQLTable
from sqlalchemy import select
from tabulate import tabulate

def gateway_outcome():
    '''Method to return the table containing the gateway outcome'''
    sqltable = SQLTable()

    #FOR PRINTING THE FINAL TABLE
    stmt = select('*').select_from(sqltable.gateway)
    result = sqltable.session.execute(stmt).fetchall()

    table = [[]]
    table.append(sqltable.gateway.columns)
    #Order by first disconnected - not checked
    for x in sorted(result, key=lambda row: row[1]): table.append(x)
    return tabulate(table, headers='firstrow', tablefmt='fancy_grid')

# converts raw data files (given in .mdb) to csv

# note: pyodbc only works on Windows machines with the Access Engine installed (pypyodbc may be an alternative)
# make sure to change the filepath to what your directory structure looks like
# edited from https://stackoverflow.com/questions/40636759/save-ms-access-tables-as-csv

import pyodbc
import csv

filename = '20150430' # change depending on input file

conn_string = ('DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ=C:\Bash\ieor_midterm\\raw\{0}.mdb'.format(filename)) 

conn = pyodbc.connect(conn_string)

cursor = conn.cursor()

cursor.execute('select * from ACCT660001;')

with open('data\{}.csv'.format(filename),'w',newline='') as f:
    writer = csv.writer(f)
    temp = [i[0] for i in cursor.description]
    writer.writerows(temp[9:]) # skip header that was split into 8 rows for some reason
    writer.writerows(cursor)

cursor.close()
conn.close()
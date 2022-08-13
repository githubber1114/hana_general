# Count the avg number of bytes/record over 1,000 records for all tables in a schema
# had to do this for an SLT Sizing

import platform
import time
from hdbcli import dbapi

# Define connection to HANA
conn = dbapi.connect(
    key='hdbuserstore entry',
    encrypt='true'
)

cursor = conn.cursor()
tbls = 0
sqlGetTbls = """
                select table_name, SUM(record_count) from m_cs_tables
                where schema_name = 'schema namr'
                group by table_name
                order by table_name
"""
cursor.execute(sqlGetTbls)
tblrows = cursor.fetchall()
for tbl in tblrows:
    cols = 0
    sqlGetCols = """
                    SELECT COLUMN_NAME FROM M_CS_COLUMNS
                    WHERE TABLE_NAME = '""" + tbl[0] + """'
                    AND SCHEMA_NAME = 'schema name'
                    AND PART_ID < 2
    """
    cursor.execute(sqlGetCols)
    rows = cursor.fetchall()
    limit=1000
    if tbl[1] < 1000:
        limit = tbl[1]
    if limit > 0:
        for row in rows:
            sqlGetRows = '''
                            SELECT top ''' + str(limit) + ''' LENGTH("''' + row[0] + '''") FROM <schema name>.''' + tbl[0]
            cursor.execute(sqlGetRows)
            lens = cursor.fetchall()
            for leng in lens:
                cols = cols + leng[0]
        print ('Table name: {}, Record count: {}, AVG record length: {} bytes'.format(tbl[0],tbl[1],cols/limit))
print('done')
cursor.close()
conn.close()

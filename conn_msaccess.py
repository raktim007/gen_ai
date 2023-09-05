import pyodbc
import streamlit as st

st.title("SQL Query Generator")

msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
st.code(f'MS-Access Drivers : {msa_drivers}')



con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
                r'DBQ=C:\Users\315604\Desktop\sql_generator\pydb1.accdb;'
conn = pyodbc.connect(con_string)

cur = conn.cursor()
cur.execute('SELECT * FROM emp')

for row in cur.fetchall():
    st.code(row)



# except pyodbc.Error as e:
#     print("Error in Connection")
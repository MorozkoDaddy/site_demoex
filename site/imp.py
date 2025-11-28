import pandas as pd
import sqlite3

print('============================')
print('_______Morozko make_______')
files = ['orders_import.xlsx', 'Tovar.xlsx', 'user_import.xlsx', 'pvz.xlsx'] # NAME TABLIC PISHI
db_name = 'database.db'
connect = sqlite3.connect(db_name)

for file in files:
    df = pd.read_excel(file)

    table_name = file.replace('.xlsx', '')  #файл - таблицааы
    df.to_sql(table_name, connect, if_exists='replace', index=False)
    print('============================')
    print(f'Table {table_name} create')
    print('============================')

connect.close()
print('Baza create!')
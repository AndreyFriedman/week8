from typing import List
from Bill import Bill
from API import get_data
from datetime import datetime

import sqlite3

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def create_table():
    cursor.execute(
        f'''CREATE TABLE {tab_name}(BillID INTEGER KEY, Name TEXT,KnessetNum INTEGER, StatusID INTEGER, PrivateNumber INTEGER unique, LastUpdatedDate SMALLDATETIME)''')
    db.commit()


def insert(bill: Bill):
    cursor.execute(
        f'''INSERT INTO {tab_name}(BillID, Name, KnessetNum, StatusID, PrivateNumber, LastUpdatedDate) VALUES(:BillID, :Name, :KnessetNum, :StatusID, :PrivateNumber, :LastUpdatedDate)''',
        bill.convert_to_dict())
    db.commit()


def print_table(num_of_rows: int = None):
    cursor.execute(f"SELECT * FROM {tab_name}")
    if num_of_rows is not None:
        rows = cursor.fetchmany(size = num_of_rows)
    else:
        rows = cursor.fetchall()
    for row in rows:
        print(f"BillID: {row[0]}")
        print(f"LastUpdatedDate: {row[1]}")
        print(f"PrivateNumber: {row[2]}")
        print(f"StatusID: {row[3]}")
        print(f"KnessetNum: {row[4]}")
        print(f"Name: {row[5]}\n")


def bill_build(data) -> List[Bill]:
    bills = []
    for data_of_bill in data:
        data = data_of_bill.get('content').get('m:properties')
        bills.append(Bill(
                BillID=int(data['d:BillID']['#text']),
                Name=str(data['d:Name']),
                KnessetNum=int(data['d:KnessetNum']['#text']),
                StatusID=int(data['d:StatusID']['#text']),
                PrivateNumber=int(data['d:PrivateNumber']['#text']),
                LastUpdatedDate=datetime.strptime(data['d:LastUpdatedDate']['#text'].split('.')[0],
                                                  DATETIME_FORMAT)
            )
        )
    return bills


data_of_bill = get_data()
bill_objects: List[Bill] = bill_build(data_of_bill)
counter = 0
for bill in data_of_bill:
        if(counter > 50):
            break
        counter = counter + 1
        print(bill)

db = sqlite3.connect("my_database.db")
cursor = db.cursor()
tab_name = "bills"

create_table()

for bill_object in bill_objects:
    insert(bill=bill_object)

print_table(num_of_rows=10)
db.close()

import os
import csv
import gzip
import happybase

def connect(host="47.103.213.21"):
    connection = happybase.Connection(host)
    return connection

def loadData(table):
    csvFile = open("mobike.csv", "w", newline="")
    writer = csv.writer(csvFile)
    writer.writerow(("bikeID", "lat", "lng"))
    for key, value in table.scan():
        writer.writerow((key.decode(), float(value[b'addr:lat'].decode()),
                         float(value[b'addr:lng'].decode())))

def lookupData(table, row_key):
    try:
        value = table.row(row_key)
        print(value)
        lng = float(value[b'addr:lng'].decode())
        lat = float(value[b'addr:lat'].decode())
        return lng, lat
    except:
        print('error row_key')
        return
    
def updateData(table, row_key, new_data):
    lookupData(table, row_key)
    table.put(row=row_key, data=new_data)
    lookupData(table, row_key)

def deleteData(table, row_key):
    lookupData(table, row_key)
    table.delete(row_key)
    lookupData(table, row_key)
  
connection = connect()
table = connection.table("mobike")
#loadData(table)
print(lookupData(table, "5516508173"))

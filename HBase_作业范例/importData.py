import os
import csv
import gzip
import happybase
import time

def un_gz(file_name):
    f_name = file_name.replace(".gz", "")
    g_file = gzip.GzipFile(file_name)
    open(f_name, "wb+").write(g_file.read())
    g_file.close()
    return f_name

def timestamp(datetime):
    timeArray = time.strptime(datetime, "%Y-%m-%dT%H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def connect(host="47.103.213.21"):
    connection = happybase.Connection(host)
    return connection

def importData(connection):
    path = "mobike/20170422"
    table = connection.table("mobike")
    gzFiles = os.listdir(path)
    for file in gzFiles:
        if file == ".DS_Store": continue
        csvPath = os.path.join(path, file)
        csvFile = un_gz(csvPath)
        csvFile = open(csvFile, "r")
        lines = csv.reader(csvFile)
        for line in lines:
            table.put(line[1], {"addr:lng":line[6], "addr:lat":line[7]},
                      timestamp=timestamp(line[0]))
            print(line)
        csvFile.close()

connection = connect()
connection.create_table("mobike", {"addr": dict(max_versions=10)})
importData(connection)

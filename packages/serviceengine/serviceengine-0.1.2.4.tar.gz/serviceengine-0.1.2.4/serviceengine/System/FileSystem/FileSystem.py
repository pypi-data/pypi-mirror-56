#!/usr/bin/python3
import json
import os.path
import urllib.request as urllib2
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd


def CreateDirIfNone(path):
    if os.path.exists(path):
        return
    os.makedirs(path)


def ReadFile(path):
    if not os.path.exists(path):
        return
    with open(path, 'r') as content_file:
        content = content_file.readlines()
        return [x.rstrip() for x in content]


def ReadSingleLine(path):
    if not os.path.exists(path):
        return
    with open(path, 'r') as content_file:
        content = content_file.readline()
        return content.rstrip()


def ReadOnlineFile(path):
    data = urllib2.urlopen(path).read().decode('utf-8')
    if data:
        data = data.split("\n")
    return data


def AppendToFile(path, data):
    file = open(path, "a+")
    for line in data:
        file.write(line)
    file.close()


def ReadJsonFile(path):
    if not os.path.exists(path):
        return
    with open(path) as json_file:
        content = json.load(json_file)
        return content


def WriteJsonFile(path, data):
    if not os.path.exists(path):
        return
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def WriteParquetFile(path, data):
    if not os.path.exists(path):
        return
    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)


def ClearFile(path):
    with open(path, 'w') as file:
        file.seek(0)
        file.truncate()


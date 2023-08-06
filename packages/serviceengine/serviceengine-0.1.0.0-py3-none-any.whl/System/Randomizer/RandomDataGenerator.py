import random
import datetime


def GetRandomjSON(schema):
    result = {}
    size = int(schema["size"])
    for att in schema["data"]:
        for i in range(size):
            type = att["type"]
            if type == "string":
                key, value = __GetRandomJsonString__(att)
                key = f"{key}_{i}" if size > 1 else key
                result[key] = value
            elif type == "int":
                key, value = __GetRandomJsonInt__(att)
                key = f"{key}_{i}" if size > 1 else key
                result[key] = value
            elif type == "list":
                key, value = __GetRandomJsonList__(att)
                key = f"{key}_{i}" if size > 1 else key
                result[key] = value
            elif type == "object":
                value = GetRandomjSON(att)
                key = f"{att['name']}_{i}" if size > 1 else att['name']

            result[key] = value
    return result


def GetRandomCSV(schema):
    result = []
    size = int(schema["size"])
    result.append(','.join([x["name"] for x in schema["data"]]))
    for i in range(size):
        row = []
        for att in schema["data"]:
            type = att["type"]
            if type == "string":
                key, value = __GetRandomJsonString__(att)
                row.append(value)
            elif type == "int":
                key, value = __GetRandomJsonInt__(att)
                row.append(value)
        result.append(','.join(row))
    return result


def __GetRandomJsonString__(schema):
    if "value" in schema:
        value = schema["value"]
    elif "options" in schema:
        value = random.choice(schema["options"])
    else:
        value = GetRandomString(int(schema["size"]))
        if "schemaPrefix" in schema:
            value = f"{schema['schemaPrefix']}{value}"
    key = schema["name"]
    return key, value


def __GetRandomJsonInt__(schema):
    if "value" in schema:
        value = schema["value"]
    elif "options" in schema:
        value = random.choice(schema["options"])
    else:
        value = GetRandomInt(int(schema["size"]))
        if "schemaPrefix" in schema:
            value = f"{schema['schemaPrefix']}{value}"
    key = schema["name"]
    return key, value


def __GetRandomJsonList__(schema):
    size = int(schema["size"])
    subType = schema["subType"] if "subType"in schema else "string"
    if "value" in schema:
        value = [schema["value"] for x in range(size)]
    elif "options" in schema:
        value = [random.choice(schema["options"]) for x in range(size)]
    else:
        value = [GetRandomString(schema["options"]) for x in range(size)] if subType == "string"\
            else [GetRandomInt(schema["options"]) for x in range(size)]
        if "schemaPrefix" in schema:
            value = [f"{schema['schemaPrefix']}{x}" for x in value]
    if subType == "Timestamp-ago":
        value = [(datetime.datetime.utcnow() - (random.random() * datetime.timedelta(hours=x)))
                     .strftime("%Y/%m/%d %H:%M:%S.%f") for x in value]
    key = schema["name"]
    return key, value

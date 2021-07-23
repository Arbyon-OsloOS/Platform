#!/usr/bin/env python3

####################################\
#        Omega Settings API         #
#   From the Omega Platform, v0.1   #
####################################/

from os import path

import yaml
import sys
import os

HOME = os.getenv("HOME")
types = {
    type("I'm a string!"): "str",
    type(23): "int",
    type(2.4): "float",
    type(True): "bool",
    type(["a", "list"]): "list",
    type(("a", "tuple")): "tuple",
    type({"key": "value"}): "dict",
    type(set()): "set"
}

class Settings():
    def __init__(self, schema="system.shared"):
        self.schema = schema
    
    def get(self, key):
        if not path.exists(HOME + "/Settings/"+self.schema+".yaml"):
            with open(HOME + "/Settings/"+self.schema+".yaml", "x") as f:
                f.write(yaml.dump({
                    "format": 0,
                    "schemas": []
                }, default_flow_style=False))
            return None
        with open(HOME + "/Settings/"+self.schema+".yaml") as f:
            data = yaml.safe_load(f.read())
        try:
            _t = data["format"] # < 1
        except KeyError:
            print("Error: can't read settings schema. Is it corrupted?")
            return None
        schemas = data["schemas"]
        for schema in schemas:
            if schema["name"] == self.schema:
                schemadata = schema
                break
        else:
            print("Error: schema %s not found." % self.schema)
            return None
        for Key in schemadata["keys"]:
            if Key["name"] == key:
                keydata = Key
                break
        else:
            print("Error: Key %s not found in schema %s." % (key, self.schema))
            return None
        return keydata["value"]
    
    def set(self, key, value):
        if not path.exists(HOME + "/Settings/"+self.schema+".yaml"):
            with open(HOME + "/Settings/"+self.schema+".yaml", "x") as f:
                f.write(yaml.dump({
                    "format": 0,
                    "schemas": []
                }, default_flow_style=False))
        with open(HOME + "/Settings/"+self.schema+".yaml") as f:
            data = yaml.safe_load(f.read())
        try:
            _t = data["format"] # < 1
        except KeyError:
            print("Error: can't read settings schema. Is it corrupted?")
            return None
        schemas = data["schemas"]
        for schema in schemas:
            if schema["name"] == self.schema:
                schemadata = schema
                break
        else:
            schemadata = {"name": self.schema, "keys": []}
            schemas.append(schemadata)
        for Key in schemadata["keys"]:
            if Key["name"] == key:
                Key["value"] = value
                Key["type"] = types[type(value)] if type(value) in types else "unknown"
                break
        else:
            schemadata["keys"].append({"name": key, "value": value,
                                       "type": types[type(value)] if type(value) in types else "unknown"})
        with open(HOME + "/Settings/"+self.schema+".yaml", 'w') as f:
            f.write(yaml.dump({"format": 0, "schemas": schemas}, default_flow_style=False))


if __name__ == "__main__":
    sys.stderr.write("This is not a script yet. Maybe in the next update...\n")
    sys.exit(1)

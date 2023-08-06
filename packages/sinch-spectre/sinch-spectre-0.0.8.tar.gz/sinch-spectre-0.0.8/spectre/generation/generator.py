import json
import os
import sys
from spectre.model import entity
from spectre.generation import api_json, proto, serializer

GENERATORS = [ api_json.generate, proto.generate ]

def generate_schema_information():
    namespace = 'com.sinch.sms.routing'
    name = 'carriers'
    base = 'routing'
    schema_info = {
        'name': name,
        'namespace': namespace,
        'base_url': base + '/api/' + name,
        'description': 'API for ' + name + ' entities'
    }
    return schema_info

def generate(path):
    with open(path, mode='r') as file:
        json_str = file.read()
        entities = json.loads(json_str)
        schema_info = generate_schema_information()
        for generator in GENERATORS:
            generator(schema_info, entities)


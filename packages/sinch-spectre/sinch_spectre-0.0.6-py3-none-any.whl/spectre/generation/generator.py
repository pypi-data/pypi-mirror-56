import json
import os
import sys
from spectre.model import entity
from spectre.generation import api_json

def generate_schema_information():
    namespace = 'smsc-routing-test'
    name = 'carriers'
    base = 'routing'
    schema_info = {
        'name': name,
        'namespace': namespace,
        'base_url': base + '/api/' + name,
        'description': 'API controller for ' + name + ' entities'
    }
    return schema_info

def generate_entities(ent):
    return entity.from_dict(ent)

def write_api_json(schema_info, entities):
    outfile = open_schema_file(schema_info)
    api_json.generate(schema_info, entities, outfile)

def persist_entities(entities):
    schema_info = generate_schema_information()
    write_api_json(schema_info, entities)

def write_template(outfile, template_path):
    print('Writing template ' + template_path + ' to ' + outfile.name)
    with open(template_path, 'r') as template_file:
        for line in template_file:
            outfile.write(line)

def open_schema_file(schema_info):
    path = generate_file_path(schema_info)
    file = open(path, 'w')
    return file

def make_directory(file_path):
    dirpath = os.path.dirname(file_path)
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

def generate_file_path(schema_info):
    path = 'out' + '/' + schema_info['name'] + '.spec'
    path = os.path.abspath(path)
    make_directory(path)
    return path

def generate(path):
    with open(path, mode='r') as file:
        json_str = file.read()
        ent = json.loads(json_str)
        #entities = generate_entities(ent)
        persist_entities(ent)
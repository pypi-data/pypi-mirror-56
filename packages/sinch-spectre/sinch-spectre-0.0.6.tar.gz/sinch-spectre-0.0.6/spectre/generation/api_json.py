import collections
import copy
import os
import re
import sys
import json
from spectre.generation.templates.api_json_template import *
from spectre.generation import serializer

TEMPLATES_PATH = 'generation/templates'

BASE_FIELDS = ['name', 'namespace', 'description', 'base_url']

REST_METHODS = { 'GET', 'POST', 'PUT' }

#map handler functions to method key
#Defined later


TEMPLATE = {
  "name": "name",
  "namespace" : "namespace",
  "description": "description",
  "base_url": "base_url",
  "info": {
    "contact": {
      "name": "contact.name",
      "email": "contact.email",
      "url": "contact.url"
    }
  },
  "imports": [
  ],
  "models": {
  },
  "resources": {
  }
}

def generate(schema_info, entities, outfile):
    try:
        spec = TEMPLATE
        set_schema_base(spec, schema_info)
        set_schema_models(spec, entities)
        set_schema_resources(spec, entities)
        print(serializer.prettify(spec))
    except Exception as e:
        print('An error occured while attempting to write file')
        print(e)

def replace_field(text, field, schema_info):
    placeholder = '%' + field + '%'
    replaced = text.replace(placeholder, schema_info[field])
    return replaced

def set_schema_base(spec_dict, schema_info):
    for field in BASE_FIELDS:
        spec_dict[field] = schema_info[field]
    return spec_dict

def set_schema_models(spec, entities):
    models = copy.deepcopy(entities)
    for ent_key in entities.keys():
        form_name = get_form_name(ent_key)
        models[form_name] = (make_form(entities[ent_key]))

    spec['models'] = models

def set_schema_resources(spec, entities):
    resources = {}
    for key in entities.keys():
        resources[key] = make_resource(entities[key], key)
    spec['resources'] = resources

def make_resource(entity, name):
    resource = { 'description': re.sub('_RESOURCE_', name, RESOURCE_DESCRIPTION)}
    operations = []
    for method in REST_METHODS:
        operations.append(make_rest_operation(entity, method, name))
    resource['operations'] = operations
    return resource
        

def make_rest_operation(entity, method, name):
    operation = { 
        'method': method,
        'description': make_rest_description(method, name)
    }

    def get(entity, operation, name):
        param_keys = ['name', 'description', 'type']
        params = []
        for f in entity['fields']:
            param = { }
            for key in param_keys:
                param[key] = f[key]
            param['required'] = False
            params.append(param)
        operation['parameters'] = params
        operation['responses'] = {
            '200': {
                'type': name
            },
            '404': {
                'type': 'string'
            }
        }
        return operation
    def post(entity, operation, name):
        operation['body'] = { 'type': get_form_name(name)}
        operation['responses'] = {
            '201': {
                'type': name
            },
            '400': {
                'type': 'string'
            }
        }
        return operation
    def put(entity, operation, name):
        return operation

    REST_HANDLER_MAP = {
        'GET': get,
        'POST': post,
        'PUT': put
    }
    
    handler = REST_HANDLER_MAP.get(method)
    #get description
    output = handler(entity, operation, name)
    return output

def make_rest_description(method, name):
    #define handler callbacks for each REST method
    def get(name):
        return 'Search for a ' + name
    def post(name):
        return 'Create a new ' + name
    def put(name):
        return 'Update a ' + name

    method_handlers = {
        'GET': get,
        'POST': post,
        'PUT': put
    }
    #get appropriate handler
    handler = method_handlers.get(method)
    #get description
    return handler(name)


def make_form(entity):
    form = copy.deepcopy(entity)
    id_pattern = r'(?:^(?:uu|gu)?id.*|.*(?:uu|gu)?id$)'
    fields = form['fields']
    for field in fields:
        name = field['name']
        if re.match(id_pattern, name):
            fields.remove(field)
            break
    return form

def get_form_name(ent_name):
    return ent_name + '_form'

def to_model(ent):
    print('Persisting ' + ent['name'])
    print(serializer.prettify(ent))
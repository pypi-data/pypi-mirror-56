import copy
import re
from spectre.generation.utils import make_form, get_form_name, to_pascal, write_to_file

def write(content, schema_info):

    outfile = f"proto/{schema_info['name']}.proto"
    write_to_file(content, outfile)

def generate(schema_info, entities):
    try:
        output = []
        output.append(create_header(schema_info))
        output.append(create_services(schema_info, entities))
        output.append(create_messages(schema_info, entities))
        write(''.join(output), schema_info)

    except Exception as e:
        print('An error occured while attempting to generate proto spec')
        print(e)

def create_header(schema_info):
    name = schema_info['name']
    output = '''
syntax = "proto3";

import "google/protobuf/struct.proto";

option java_multiple_files = true;
option java_package = "__JAVA_PACKAGE__";
option java_outer_classname = "Grpc";

package __PACKAGE__;
'''
    output = output.replace('__JAVA_PACKAGE__', schema_info['namespace'] + '.' + name + '.grpc')
    output = output.replace('__PACKAGE__', schema_info['namespace'] + '.' + name)
    return output

def create_messages(schema_info, entities):

    def create_message(entity, name):
        OUTPUT = ['message ' + to_pascal(name) + ' {']
        FIELD_COUNTER = 1
        def add(addition):
            OUTPUT.append('\n\t' + addition)

        def make_field(field):
            field_type, rep = convert_type(field['type'])
            field_name = field['name']
            repeated = 'repeated ' if rep else ''
            default_val = field.get('default', '')
            #Don't set default value for required fields
            default = f' [default = {default_val}]' if default_val and not req else ''
            nonlocal FIELD_COUNTER
            output = f'{repeated}{field_type} {field_name} = {FIELD_COUNTER}{default};'
            FIELD_COUNTER += 1
            return output

        for field in entity['fields']:
            add(make_field(field))

        OUTPUT.append('\n}')
        return ''.join(OUTPUT)
    
    output = []

    messages = copy.deepcopy(entities)

    for key in entities.keys():
        form_name = get_form_name(key)
        messages[form_name] = make_form(entities[key])

    for key in messages.keys():
        message = create_message(messages[key], key)
        output.append('\n' + message + '\n')
    return ''.join(output)

def convert_type(t):
    type_map = {
        'int': 'int32',
        'uuid': 'string',
        'guid': 'string',
        '': "TYPE_MISSING"
    }
    repeated = True if '[' in t else False
    field_type = re.sub('[\[\]]', '', t)
    #Return mapped value if present, otherwise default to given type
    field_type = type_map.get(field_type, field_type)
    
    return field_type, repeated


def create_services(schema_info, entities):

    def make_crud(name):
        OUTPUT = []

        def add(addition):
            OUTPUT.append(f'\n\trpc {addition};')

        add(f'create({to_pascal(get_form_name(name))}) returns ({name})')
        add(f'retrieve({name}) returns ({name})')
        add(f'update({name}) returns ({name})')
        #No delete for now
        #add(f'delete({name}) returns (statusPlaceholderType)')
        return OUTPUT

    def create_service(entity, name):
        name = to_pascal(name)
        service = ['service ' + name + 'Service {']
        service.extend(make_crud(name))
        service.append('\n}\n')

        return ''.join(service)

    services = []

    for key in entities.keys():
        services.append('\n' + create_service(entities[key], key))
    return ''.join(services)

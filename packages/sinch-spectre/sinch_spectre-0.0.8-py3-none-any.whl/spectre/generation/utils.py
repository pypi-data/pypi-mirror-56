import os
import re
import copy

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

def to_pascal(text):
    words = text.split('_')
    output = []
    for word in words:
        output.append(word[0].upper() + word[1:])
    return ''.join(output)

def write_to_file(content, outfile):

    out_dir = 'out'

    def get_file_path(outfile):
        path = f'{out_dir}/{outfile}'
        path = os.path.abspath(path)
        return path

    def make_directory(file_path):
        dirpath = os.path.dirname(file_path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

    file_path = get_file_path(outfile)
    make_directory(file_path)
    try:
        with open(file_path, 'w') as outfile:
            outfile.write(content)
    except:
        print(f'I/O error while writing {file_path}')
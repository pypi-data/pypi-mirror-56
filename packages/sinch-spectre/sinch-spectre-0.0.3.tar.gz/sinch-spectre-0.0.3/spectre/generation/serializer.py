import jsonpickle
import json
import sys
from collections import OrderedDict
sys.path.append(sys.path[0] + '/..')

def to_json(obj):
    return jsonpickle.encode(obj)

def from_json(json_obj):
    return jsonpickle.decode(json_obj)

def prettify(json_obj):
    return json.dumps(json_obj, sort_keys=False,
                 indent=4, separators=(',', ': '))
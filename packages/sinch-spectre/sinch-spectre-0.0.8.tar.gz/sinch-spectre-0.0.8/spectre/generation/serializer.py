import json
import sys
from collections import OrderedDict

def prettify(json_obj):
    return json.dumps(json_obj, sort_keys=False,
                 indent=4, separators=(',', ': '))
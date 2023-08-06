import argparse
import os
import sys
import subprocess

def handle_resource():
    print('resource not implemented')

modules = {
    'entity': 'entity.py',
    'resource': handle_resource,
}

#Set up arguments
parser = argparse.ArgumentParser(description = 'Manage your API specification and its entitites')
parser.add_argument('module', choices=modules.keys())
parser.add_argument('commands', nargs='*')
args = parser.parse_args()
#Get executing dir of the script (CLI dir)
script_dir = sys.path[0]

handler = script_dir + '/' + modules.get(args.module)
#Open respective module handler
subprocess.Popen([sys.executable, handler] + args.commands)
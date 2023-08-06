from __future__ import print_function, unicode_literals
import argparse
from PyInquirer import prompt
from pprint import pprint

def add():
    print('Adding a new entity')
    questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
     }
]

def main():
    answers = prompt(questions)
    pprint(answers)

    commands = {
        'add': add,
    }

    parser = argparse.ArgumentParser(description = 'Manage your entity specifications')
    parser.add_argument('command', choices=['add', 'edit'])

    args = parser.parse_args()

    handler = commands[args.command]
    handler()
  
main()


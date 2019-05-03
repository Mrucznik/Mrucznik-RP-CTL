import os
import json
from PyInquirer import prompt

from mrucznikctl.config import groups, parameterTypes, get_default_parameter_description, get_default_parameter_name
from mrucznikctl.validators import NameValidator, VariableValidator


def create_command(args):
    print('Witaj w narzędziu tworzącym komendę dla mapy Mrucznik Role Play')

    command = command_creator()

    if not os.path.exists(command['name']):
        os.mkdir(command['name'])

    command_name = '{0}/{0}.json'.format(command['name'])
    with open(command_name, 'w') as file:
        json.dump(command, file, indent=4)
    print('Komenda pomyślnie utworzona jako plik {}'.format(command_name))

    return command


def command_creator():
    questions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Jak ma nazywać się komenda?',
            'validate': NameValidator
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Wpisz opis komendy, który będzie widoczny dla graczy:',
        },
        {
            'type': 'checkbox',
            'name': 'permissions',
            'message': 'Wybierz, które grupy mają mieć dostęp do komendy:',
            'choices': groups
        },
        {
            'type': 'input',
            'name': 'author',
            'message': 'Kto jest autorem komendy?'
        },
        {
            'type': 'confirm',
            'name': 'aliases',
            'message': 'Czy komenda będzie miała dodatkowe aliasy?'
        }
    ]

    answers = prompt(questions)

    if answers['aliases']:
        answers['aliases'] = command_aliases()
    else:
        answers['aliases'] = []

    answers.update(prompt([
        {
            'type': 'confirm',
            'name': 'parameters',
            'message': 'Czy komenda będzie posiadała parametry?'
        }])
    )

    if answers['parameters']:
        answers['parameters'] = command_parameters()
    else:
        answers['parameters'] = []

    return answers


def command_aliases():
    aliases = []
    next_element = True
    while next_element:
        questions = [
            {
                'type': 'input',
                'name': 'alias',
                'message': 'Wpisz alias:',
                'validate': NameValidator
            },
            {
                'type': 'confirm',
                'name': 'next',
                'message': 'Dodać następny alias?'
            }
        ]
        answers = prompt(questions)
        next_element = answers.pop('next')
        aliases.append(answers['alias'])

    return aliases


def command_parameters():
    parameters = []
    next_element = True
    while next_element:
        answers = prompt(
            {
                'type': 'list',
                'name': 'type',
                'message': 'Wybierz typ parametru:',
                'choices': parameterTypes
            }
        )

        questions = []
        if answers['type'] == 'string':
            questions.append(
                {
                    'type': 'input',
                    'name': 'size',
                    'message': 'Wpisz rozmiar ciągu znaków:',
                    'default': get_default_parameter_description(answers['type'])
                }
            )

        questions.append(
            {
                'type': 'input',
                'name': 'name',
                'message': 'Wpisz nazwę parametru:',
                'default': get_default_parameter_name(answers['type']),
                'validate': VariableValidator
            }
        )
        questions.append(
            {
                'type': 'input',
                'name': 'description',
                'message': 'Wpisz opis parametru:',
                'default': get_default_parameter_description(answers['type'])
            }
        )
        questions.append(
            {
                'type': 'confirm',
                'name': 'default',
                'message': 'Czy parametr powinien mieć wartość domyślną?',
            }
        )

        answers.update(prompt(questions))

        if answers.pop('default'):
            answers.update(prompt([
                {
                    'type': 'input',
                    'name': 'defaultValue',
                    'message': 'Wpisz wartość domyślną:'
                }
            ]))

        answers.update(prompt([
            {
                'type': 'confirm',
                'name': 'next',
                'message': 'Dodać następny parametr?'
            }
        ]))
        next_element = answers.pop('next')
        parameters.append(answers)

    return parameters
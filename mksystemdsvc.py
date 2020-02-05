#!/usr/bin/env python3

import argparse
import shutil
from prompt_toolkit import prompt, HTML, print_formatted_text as print
from prompt_toolkit.validation import Validator, ValidationError
from elevate import elevate
from pathlib import Path
from string import Template


class RequiredValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(
                message='This propery is required')


class RestartNumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(
                message='This propery is required')

        if text.isdigit():
            integer = int(text)
            if integer < 1 or integer > 6:
                raise ValidationError(
                    message='Please choose a number between 1 and 6')

        if not text.isdigit():
            raise ValidationError(
                message='This input contains non-numeric characters')


class ServiceLocationValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(
                message='This propery is required')

        if text.isdigit():
            integer = int(text)
            if integer < 1 or integer > 2:
                raise ValidationError(
                    message='Please choose a number between 1 and 2')

        if not text.isdigit():
            raise ValidationError(
                message='This input contains non-numeric characters')


def generate_unit(svcname, executable, cwddir, usraccount, usrgroup, restart, desc):
    template = Template(open("template.service", "r").read())

    restart_mapping = {
        1: 'no',
        2: 'always',
        3: 'on-success',
        4: 'on-failure',
        5: 'on-abnormal',
        6: 'on-abort',
        7: 'on-watchdog'
    }

    restartcmd = restart_mapping.get(int(restart))

    output = template.substitute(description=desc, user=usraccount,
                                 group=usrgroup, workingdir=cwddir, exec=executable, name=svcname, restart=restartcmd)
    filename = f'{svcname}.service'
    with open(filename, mode='w') as servicefile:
        servicefile.write(output)
    print(f"Written service file to {filename}")
    return filename


def install_unit(unit):
    base_path = Path('/etc/systemd')
    location_mapping = {
        1: 'system',
        2: 'user',
    }

    location_choice = prompt(
        'Do you want to install a service for your system or for a local user? (1 = system install, 2 = user install)', validator=ServiceLocationValidator())

    final_path = base_path / location_mapping.get(int(location_choice))
    shutil.copy2(unit, final_path)

    print(f"Service file installed to {final_path}")


def main():
    print(HTML('<b><skyblue>systemd unit file generator</skyblue></b>'))

    unit_install = False

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--install', help='Install the generated systemd file. You need root rights or sudo to use this option.')
    args = argparser.parse_args()
    if args.install:
        elevate()
        unit_install = True

    svcname = prompt('Service name: ', validator=RequiredValidator())
    executable = prompt('Service command: ',
                        validator=RequiredValidator())
    cwddir = prompt('Working directory: ')
    usraccount = prompt('Service account name: ',
                        validator=RequiredValidator())
    usrgroup = prompt('Service group name: ')
    restart = prompt(
        'Restart Behavior (1 = never, 2 = always 3 = on-success 4 = on-failure 5 = on-abnormal 6 = on-abort 7 = on-watchdog): ', validator=RestartNumberValidator())
    desc = prompt('Description: ')

    file = generate_unit(svcname, executable, cwddir,
                         usraccount, usrgroup, restart, desc)

    if unit_install:
        install_unit(file)


if __name__ == "__main__":
    main()

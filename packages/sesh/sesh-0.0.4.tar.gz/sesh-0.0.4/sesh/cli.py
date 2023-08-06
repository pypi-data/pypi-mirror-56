"""
Sesh is a tool for managing music classes from the command line.
Copyright (C) 2019  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com

This module should handle all of the command-line parsing and
invoke the correct command in the api module.
"""

import argparse

from sesh.__version__ import __version__


# create the top-level parser
parser = argparse.ArgumentParser(
    prog='sesh',
    description='Use sesh to manage Music Center classes and rentals.',
    conflict_handler='resolve',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='\n \n',
)

parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s ' + f'version { __version__}'
)

# Add subparser below for each sesh command
subparsers = parser.add_subparsers(
    title='sesh commands',
)


# create the parser for the "admin" command
parser_admin = subparsers.add_parser(
    'admin',
    help=(
        'This is the only command that may be used without logging-in first.\n'
        'This is used to perform administrative functions on the Sesh\n'
        'database itself. A Staff member login will be required to perform\n'
        'these actions in future versions of Sesh.\n\n'
    )
)

parser_admin.add_argument(
    '--init-db',
    action='store_true',
    dest='init_db',
    help='Initialize a new database. Any existing database will be deleted!'
)

parser_admin.add_argument(
    '--load-sample-data',
    action='store_true',
    dest='load_sample_data',
    help='Load some sample data into the database.'
)

parser_admin.set_defaults(cmd='admin')


# create the parser for the "delete" command
parser_delete = subparsers.add_parser(
    'delete',
    help='help for delete command'
)

parser_delete.add_argument(
    'target',
    choices=[
        'classroom',
        'instrument',
        'role',
        'user',
    ],
)

parser_delete.set_defaults(cmd='delete')


# create the parser for the "login" command
parser_login = subparsers.add_parser(
    'login',
    help='help for login command'
)

parser_login.set_defaults(cmd='login')


# create the parser for the "logout" command
parser_logout = subparsers.add_parser(
    'logout',
    help='help for logout command'
)

parser_logout.set_defaults(cmd='logout')


# create the parser for the "new" command
parser_new = subparsers.add_parser(
    'new',
    help='help for new command'
)

parser_new.add_argument(
    'target',
    choices=[
        'classroom',
        'instrument',
        'role',
        'user',
    ],
)

parser_new.set_defaults(cmd='new')


# create the parser for the "update" command
parser_update = subparsers.add_parser(
    'update',
    help='help for update command'
)

parser_update.add_argument(
    'target',
    choices=[
        'classroom',
        'instrument',
        'role',
        'user',
    ],
)

parser_update.set_defaults(cmd='update')


# create the parser for the "rent" command
parser_rent = subparsers.add_parser(
    'rent',
    help='help for rent command'
)

parser_rent.add_argument(
    'action',
    choices=[
        'start',
        'stop',
    ],
)

parser_rent.set_defaults(cmd='rent')


# create the parser for the "show" command
parser_show = subparsers.add_parser(
    'show',
    formatter_class=argparse.RawTextHelpFormatter,
    help='help for the show command'
)

parser_show.add_argument(
    'report',
    choices=[
        'accounts',
        'instruments',
        'schedule',
        'user',
    ],
    metavar='report',
    help=(
        'The type of report to show.\n'
        'Choices include accounts, instruments, schedule, or user.\n'
    )
)

parser_show.add_argument(
    'qualifier',
    nargs='*',
)

parser_show.add_argument(
    '--csv',
    action='store_true',
    dest='csv',
    help='Save report to a CSV file.'
)

parser_show.add_argument(
    '--json',
    action='store_true',
    dest='json',
    help='Save report to a JSON file.'
)

parser_show.set_defaults(cmd='show')

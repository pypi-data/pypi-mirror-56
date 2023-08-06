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
"""

from sesh import core
from sesh.init_db import _init_db

__all__ = ['admin', 'delete', 'login', 'logout', 'new', 'show', 'update']


def admin(args, kwargs=None):
    if args.init_db:
        _init_db()


def delete(args, kwargs=None):
    pass


def login(args, kwargs=None):
    print("\nLogging in...\n\n")


def logout(args, kwargs=None):
    print("\nLogging out...\n\n")


def new(args, kwargs=None):
    pass


def rent():
    pass


def show(args, kwargs=None):
    print(f"\nARGS: {args}\n\n")
    pass


def update(args, kwargs=None):
    pass

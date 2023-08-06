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


class User(object):
    """docstring for User"""

    def __init__(self, args, kwargs):
        self._id = None
        self._role = kwargs.get('role')
        self._name_first = kwargs.get('name_first')
        self._name_last = kwargs.get('name_last')
        self._addr1 = kwargs.get('addr1')
        self._addr2 = kwargs.get('addr2')
        self._addr_city = kwargs.get('addr_city')
        self._addr_state = kwargs.get('addr_state')
        self._addr_zip = kwargs.get('addr_zip')
        self._email = kwargs.get('email')
        self._phone = kwargs.get('phone')
        self._login = kwargs.get('login')


class Instructor(User):
    """docstring for Instructor"""

    def __init__(self, args, kwargs):
        super(Instructor, self).__init__(*args, **kwargs)
        self._specialties = kwargs.get('specialties')
        self._availability = kwargs.get('availability')


class Staff(User):
    """docstring for Staff"""

    def __init__(self, args, kwargs):
        super(Staff, self).__init__(*args, **kwargs)
        self._title = kwargs.get('title')


class Student(User):
    """docstring for Student"""

    def __init__(self, args, kwargs):
        super(Student, self).__init__(*args, **kwargs)
        self._account_balance = kwargs.get('account_balance')
        self._instruments = kwargs.get('instruments')

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

from hashlib import sha256
import random
import sqlite3
import string
from textwrap import dedent

from sesh.config.base_config import SESH_DB_PATH, SESH_ADMIN_FILE
from sesh.error import ExitCode


def _init_db():
    # If there is an existing database, delete it.
    if SESH_DB_PATH.exists():
        SESH_DB_PATH.unlink()
    _create_tables()
    _create_default_data()

    return ExitCode.EX_SUCCESS


def _create_tables():
    conn = sqlite3.connect(SESH_DB_PATH)
    c = conn.cursor()
    c.executescript(
        """
        CREATE TABLE "role"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "role_id" INTEGER NOT NULL UNIQUE,
            "name" VARCHAR(32) NOT NULL,
            "description" VARCHAR(300) NOT NULL
        );

        CREATE TABLE "user"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "role_id" INTEGER NOT NULL
                REFERENCES "role" ("role_id") DEFERRABLE INITIALLY DEFERRED,
            "name_first" VARCHAR(30) NOT NULL,
            "name_last" VARCHAR(60) NOT NULL,
            "addr1" VARCHAR(250),
            "addr2" VARCHAR(250),
            "addr_city" VARCHAR(64),
            "addr_state" VARCHAR(2),
            "addr_zip" VARCHAR(20),
            "email" VARCHAR(250) NOT NULL,
            "phone" VARCHAR(12),
            "password" VARCHAR(128) NOT NULL
        );

        CREATE TABLE "specialty"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "specialty" VARCHAR(64) NOT NULL
        );

        CREATE TABLE "instructor_spec"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "specialty" INTEGER NOT NULL
                REFERENCES "specialty" ("id") DEFERRABLE INITIALLY DEFERRED
        );

        CREATE TABLE "instructor_avail"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "day_of_week" VARCHAR(9) NOT NULL,
            "time_start" VARCHAR(32) NOT NULL,
            "time_end" VARCHAR(32),
            "active" BOOLEAN NOT NULL DEFAULT 1
        );

        CREATE TABLE "staff"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "title" VARCHAR(32)
        );

        CREATE TABLE "student"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "account_balance" DOUBLE,
            "instruments" VARCHAR(250)
        );

        CREATE TABLE "classroom"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "recording_capable" BOOLEAN NOT NULL DEFAULT 0,
            "location" VARCHAR(32)
        );

        CREATE TABLE "classroom_avail"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "classroom_id" INTEGER NOT NULL
                REFERENCES "classroom" ("id") DEFERRABLE INITIALLY DEFERRED,
            "day_of_week" VARCHAR(9) NOT NULL,
            "time_start" VARCHAR(32) NOT NULL,
            "time_end" VARCHAR(32),
            "active" BOOLEAN NOT NULL DEFAULT 1
        );

        CREATE TABLE "instrument"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "type" VARCHAR(32) NOT NULL,
            "model" VARCHAR(32) NOT NULL,
            "inv_tag" VARCHAR(64) NOT NULL UNIQUE,
            "rental_fee" DOUBLE NOT NULL
        );

        CREATE TABLE "rental"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "inv_tag" INTEGER NOT NULL
                REFERENCES "instrument" ("inv_tag")
                DEFERRABLE INITIALLY DEFERRED,
            "user_id" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "date_start" DATETIME NOT NULL,
            "date_end" DATETIME
        );

        CREATE TABLE "class_session"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "instructor" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "student" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "classroom" INTEGER NOT NULL
                REFERENCES "classroom" ("id") DEFERRABLE INITIALLY DEFERRED,
            "date" DATETIME NOT NULL,
            "time_start" TIME NOT NULL,
            "session_lenth" REAL NOT NULL,
            "instrument" INTEGER NOT NULL
                REFERENCES "instrument" ("id") DEFERRABLE INITIALLY DEFERRED,
            "recording" BOOLEAN NOT NULL DEFAULT 0,
            "canelled" BOOLEAN NOT NULL DEFAULT 0,
            "amt_billed" DOUBLE NOT NULL DEFAULT 0.00,
            "amt_paid" DOUBLE NOT NULL DEFAULT 0.00
        );

        CREATE TABLE "login_session"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL
                REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "time_login" TIMESTAMP NOT NULL,
            "time_last_cmd" TIMESTAMP,
            "time_logout" TIMESTAMP
        );
        """
    )
    conn.close()


def _create_default_data():
    _create_default_instrument()
    _create_default_roles()
    _create_default_user()
    _create_default_specialties()


def _create_default_instrument():
    conn = sqlite3.connect(SESH_DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO "instrument" ("type", "model", "inv_tag", "rental_fee")
        VALUES ("Student Owned", "Unknown", "NONE", 0.00)
        """)
    conn.commit()
    conn.close()


def _create_default_roles():
    default_roles = [
        (1, "Staff", "Music Center Administrative Staff"),
        (2, "Instructor", "Music Center Instructor"),
        (3, "Student", "Music Center Student")
    ]
    conn = sqlite3.connect(SESH_DB_PATH)
    c = conn.cursor()
    c.executemany("""
        INSERT INTO "role" ("role_id", "name", "description")
        VALUES (?, ?, ?)
        """, default_roles)
    conn.commit()
    conn.close()


def _create_default_user():
    role_id = 1
    name_first = "Admin"
    name_last = "ChangeMe"
    email = "admin@example.com"
    pw_length = 12
    pw = ''.join(
        random.choices(
            string.ascii_letters +
            string.digits +
            string.punctuation,
            k=pw_length
        ))
    pw_hash = sha256(pw.encode('utf-8')).hexdigest()

    with open(SESH_ADMIN_FILE, 'w') as f:
        f.write(pw)

    conn = sqlite3.connect(SESH_DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO "user"
            ("role_id", "name_first", "name_last", "email", "password")
        VALUES (?, ?, ?, ?, ?)
        """, (role_id, name_first, name_last, email, pw_hash))

    c.execute("""
        INSERT INTO "staff" ("user_id", "title")
        VALUES (?, ?)
        """, (c.lastrowid, "Staff Administrator"))
    conn.commit()
    conn.close()

    print(dedent(
        f"""

        An admin user has been created in the database.
        The initial password for this user can be found in the file
        located at {SESH_ADMIN_FILE}.

        The login name is {email}

        Please login now and update that user with your information and
        change the password!!!


        """
    ))


def _create_default_specialties():
    default_specialties = [
        ("Cello",),
        ("Clarinet",),
        ("Didgeridoo",),
        ("Guitar",),
        ("Percussion",),
        ("Piano",),
        ("Saxophone",),
        ("Trumpet",),
        ("Violin",),
        ("Voice",)
    ]
    conn = sqlite3.connect(SESH_DB_PATH)
    c = conn.cursor()
    c.executemany("""
        INSERT INTO "specialty" ("specialty")
        VALUES (?)
        """, default_specialties)
    conn.commit()
    conn.close()


def _get_conn_cursor():
    conn = sqlite3.connect(SESH_DB_PATH)
    cursor = conn.cursor()

    return conn, cursor


def _load_sample_data():
    conn, cursor = _get_conn_cursor()

    _load_sample_staff(conn, cursor)
    _load_sample_instructors(conn, cursor)
    _load_sample_students(conn, cursor)
    _load_sample_instruments(conn, cursor)
    _load_sample_rentals(conn, cursor)
    _load_sample_classrooms(conn, cursor)
    _load_sample_class_sessions(conn, cursor)

    conn.close()


def _load_sample_user(conn, cursor, user):
    cursor.execute(
        """
        INSERT INTO "user"(
            "role_id",
            "name_first",
            "name_last",
            "addr1",
            "addr2",
            "addr_city",
            "addr_state",
            "addr_zip",
            "email",
            "phone"
            "password"
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        user
    )
    conn.commit()

    return cursor.lastrowid


def _load_sample_staff(conn, cursor):
    # Sample user password is mUs1caL*
    sample_staff_users = [
        (
            1,
            "Jeffrey",
            "Lebowski",
            "1642 Sunset Boulevard",
            None,
            "Los Angeles",
            "CA",
            "90210",
            "one.chillindude@live.com",
            "310-848-9325‬"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        ),
        (
            1,
            "Kurt",
            "Gödel",
            "1 Einstein Drive",
            None,
            "Princeton",
            "NJ",
            "08540",
            "kgodel@live.com",
            "703-821-9316‬"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        ),
        (
            1,
            "Margot",
            "Tenenbaum",
            "Central Park West at 79th Street",
            None,
            "New York",
            "NY",
            "10024",
            "margot.frolics@outlook.com",
            "703-506-9102"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        )
    ]

    sample_titles = [
        "Owner",
        "Accountant",
        "Head Instructor"
    ]

    for i, user in enumerate(sample_staff_users):
        user_id = _load_sample_user(conn, cursor, user)
        cursor.execute(
            """
            INSERT INTO "staff" ("user_id", "title")
            VALUES (?, ?)
            """,
            (user_id, sample_titles[i])
        )
        conn.commit()


def _load_sample_instructors(conn, cursor):
    # Sample user password is mUs1caL*
    sample_instructor_users = [
        (
            2,
            "Nathan",
            "Muir",
            "8200 Georgetown Pike",
            None,
            "McLean",
            "VA",
            "22102",
            "old.scotch@outlook.com",
            "703-656-6916‬"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        ),
        (
            2,
            "Tom",
            "Bishop",
            "11110 Georgetown Pike",
            None,
            "Great Falls",
            "VA",
            "22066",
            "smugglebishop@yahoo.com",
            "‭703-255-1001"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        ),
        (
            2,
            "Ziva",
            "David",
            "1051 Waverly Way",
            None,
            "McLean",
            "VA",
            "22101",
            "ziva.sings@yahoo.com",
            "‭703-821-0022‬"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        )
    ]

    specialties = [
        ["[]", "{}"],
        ["[]", "{}"],
        ["[]", "{}"]
    ]

    for i, user in enumerate(sample_instructor_users):
        user_id = _load_sample_user(conn, cursor, user)
        cursor.execute(
            """
            INSERT INTO "instructor" ("user_id", "specialties", "availability")
            VALUES (?, ?, ?)
            """,
            (user_id, specialties[i])
        )
        conn.commit()


def _load_sample_students(conn, cursor):
    # Sample user password is mUs1caL*
    sample_staff_users = [
        (
            3,
            "Jeffrey",
            "Lebowski",
            "1642 Sunset Boulevard",
            None,
            "Los Angeles",
            "CA",
            "90210",
            "one.chillindude@live.com",
            "310-848-9325‬"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        ),
        (
            3,
            "name_first",
            "name_last",
            "addr1",
            "addr2",
            "addr_city",
            "addr_state",
            "addr_zip",
            "email",
            "phone"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        ),
        (
            3,
            "name_first",
            "name_last",
            "addr1",
            "addr2",
            "addr_city",
            "addr_state",
            "addr_zip",
            "email",
            "phone"
            "f8691f96be6422505f3a0078c8071b1b0e0201356b20168804436bd26431ae39"
        )
    ]

    sample_titles = [
        "Owner",
        "Accountant",
        "Head Instructor"
    ]

    for i, user in enumerate(sample_staff_users):
        user_id = _load_sample_user(conn, cursor, user)
        cursor.execute(
            """
            INSERT INTO "staff" ("user_id", "title")
            VALUES (?, ?)
            """,
            (user_id, sample_titles[i])
        )
        conn.commit()


def _load_sample_instruments(conn, cursor):
    pass


def _load_sample_rentals(conn, cursor):
    pass


def _load_sample_classrooms(conn, cursor):
    pass


def _load_sample_class_sessions(conn, cursor):
    pass

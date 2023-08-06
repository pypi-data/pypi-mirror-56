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
    c.executescript("""
        CREATE TABLE "role"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "role_id" INTEGER NOT NULL UNIQUE,
            "name" VARCHAR(32) NOT NULL,
            "description" VARCHAR(300) NOT NULL
        );

        CREATE TABLE "user"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "role_id" INTEGER NOT NULL REFERENCES "role" ("role_id") DEFERRABLE INITIALLY DEFERRED,
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

        CREATE TABLE "instructor"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "specialties" VARCHAR(500),
            "availability" VARCHAR(1000)
        );

        CREATE TABLE "staff"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "title" VARCHAR(32)
        );

        CREATE TABLE "student"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "account_balance" DOUBLE,
            "instruments" VARCHAR(250)
        );

        CREATE TABLE "classroom"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "recording_capable" BOOLEAN NOT NULL DEFAULT 0,
            "location" VARCHAR(32)
        );

        CREATE TABLE "instrument"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "type" VARCHAR(32) NOT NULL,
            "model" VARCHAR(32) NOT NULL,
            "inv_tag" VARCHAR(64) NOT NULL,
            "rental_fee" DOUBLE NOT NULL
        );

        CREATE TABLE "rental"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "inv_tag" INTEGER NOT NULL REFERENCES "instrument" ("id") DEFERRABLE INITIALLY DEFERRED,
            "user_id" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "date_start" DATETIME NOT NULL,
            "date_end" DATETIME
        );

        CREATE TABLE "class_session"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "instructor" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "student" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "classroom" INTEGER NOT NULL REFERENCES "classroom" ("id") DEFERRABLE INITIALLY DEFERRED,
            "date" DATETIME NOT NULL,
            "time_start" TIME NOT NULL,
            "session_lenth" REAL NOT NULL,
            "instrument" INTEGER NOT NULL REFERENCES "instrument" ("id") DEFERRABLE INITIALLY DEFERRED,
            "recording" BOOLEAN NOT NULL DEFAULT 0,
            "canelled" BOOLEAN NOT NULL DEFAULT 0,
            "amt_billed" DOUBLE NOT NULL DEFAULT 0.00,
            "amt_paid" DOUBLE NOT NULL DEFAULT 0.00
        );

        CREATE TABLE "login_session"(
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "time_login" TIMESTAMP NOT NULL,
            "time_last_cmd" TIMESTAMP,
            "time_logout" TIMESTAMP
        );
    """)
    conn.close()


def _create_default_data():
    _create_default_instrument()
    _create_default_roles()
    _create_default_user()


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
        INSERT INTO "user" ("role_id", "name_first", "name_last", "email", "password")
        VALUES (?, ?, ?, ?, ?)
        """, (role_id, name_first, name_last, email, pw_hash))

    c.execute("""
        INSERT INTO "staff" ("user_id", "title")
        VALUES (?, ?)
        """, (c.lastrowid, "Staff Administrator"))
    conn.commit()
    conn.close()

    # print(
    #     f"\nAn admin user has been created in the database.\n"
    #     f"The initial password for this user can be found in the file\n"
    #     f"located at {SESH_ADMIN_FILE}.\n\n"
    #     f"The login name is {email}\n\n"
    #     f"Please login now and update that user with your information and\n"
    #     f"change the password!!!\n\n"
    # )

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


def _load_test_data():
    pass

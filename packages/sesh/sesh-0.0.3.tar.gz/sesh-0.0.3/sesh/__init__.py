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


    sesh [args] [<command>] [<args>]

"""

from sesh import api
from sesh.cli import parser
from sesh.error import ExitCode
from sesh.log import get_logger

logger = get_logger(__name__)


def main():
    """Run `sesh` command
    If the user calls `sesh --help`, or `sesh COMMAND` with out the expected
    COMMAND arguments, the parser will catch this in the parser.parse_args()
    method and then print the Help and exit before going any further
    in the main() function.

    The 'check' that is performed in main() ensures that if the user runs
    `sesh` without *any* arguments, the Help will still be displayed.
    """
    """Setup logging configuration."""
    args = parser.parse_args() or None
    logger.info(f"cli args: {vars(args)}")

    if len(vars(args)) > 0:
        try:
            getattr(api, args.cmd)(args)
        except SystemExit as e:
            return e.code
        else:
            return ExitCode.EX_SUCCESS
    else:
        parser.print_help()
        return ExitCode.EX_USAGE

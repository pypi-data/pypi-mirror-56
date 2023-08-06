# -*- coding: utf-8 -*-
# davpoint - Davfs2 wrapper to mount SharePoint filesystems
# Copyright © 2019 Damien Goutte-Gattat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import sys

from incenp.davpoint import __version__
from incenp.davpoint.compat import ConfigParser
from incenp.davpoint.davfs2 import get_credentials, mount
from incenp.davpoint.sharepoint import authenticate


prog_name = "davpoint"
prog_notice = """\
{} {}
Copyright © 2019 Damien Goutte-Gattat

This program is released under the GNU General Public License.
See the COPYING file or <http://www.gnu.org/licenses/gpl.html>.
""".format(prog_name, __version__)


def die(msg):
    sys.stderr.write("{}: {}\n".format(prog_name, msg))
    sys.exit(1)


class VersionAction(argparse.Action):

    def __init__(self, option_strings, dest):
        super(VersionAction, self).__init__(
                option_strings, dest, nargs=0,
                help="Show information about the program and exit")

    def __call__(self, parser, namespace, values, option_string=None):
        parser.exit(prog_notice)


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]

    home_dir = os.getenv('HOME', default='')
    conf_dir = '{}/.davfs2'.format(home_dir)

    parser = argparse.ArgumentParser(
                        prog=prog_name,
                        description="Mount SharePoint remote filesystems.",
                        epilog="Report bugs to <devel@incenp.org>.")
    parser.add_argument('-v', '--version', action=VersionAction)
    parser.add_argument('-c', '--config',
                        default='{}/sharepoint.conf'.format(conf_dir),
                        help="path to an alternative configuration file")
    parser.add_argument('share', help="name of the share to mount")

    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    if not config.has_section(args.share):
        die("No section '{}' in configuration file".format(args.share))

    endpoint = config.get(args.share, 'endpoint')
    mountpoint = config.get(args.share, 'mountpoint')

    davfs2_options = {}
    for key, value in config.items(args.share):
        if key not in ('endpoint', 'mountpoint'):
            davfs2_options[key] = value

    username, password = get_credentials(endpoint, mountpoint)
    cookies = authenticate(endpoint, username, password)
    davfs2_options['add_header'] = 'Cookie rtFa={rtFa};FedAuth={FedAuth};'.format(**cookies)

    mount(mountpoint, davfs2_options)


if __name__ == '__main__':
    main()

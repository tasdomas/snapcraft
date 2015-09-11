# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

import snapcraft


class Python3ProjectPlugin(snapcraft.BasePlugin):

    # note that we don't need to setup env(), python figures it out
    # see python3.py for more details

    def pull(self):
        return self.handle_source_options()

    def build(self):
        # If setuptools is used, it tries to create files in the
        # dist-packages dir and import from there, so it needs to exist
        # and be in the PYTHONPATH. It's harmless if setuptools isn't
        # used.
        os.makedirs(self.dist_packages_dir, exist_ok=True)
        env = os.environ.copy()
        env["PYTHONPATH"] = self.dist_packages_dir
        return self.run(
            ["python3", "setup.py", "install", "--install-layout=deb",
             "--prefix=%s/usr" % self.installdir],
            env=env)

    @property
    def dist_packages_dir(self):
        return self.installdir + "/usr/lib/python3/dist-packages"

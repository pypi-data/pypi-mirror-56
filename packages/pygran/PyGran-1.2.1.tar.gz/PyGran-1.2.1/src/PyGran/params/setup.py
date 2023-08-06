'''
  Created on Oct 08, 2019
  Author: Andrew Abi-Mansour

  This is the::

  ██████╗ ██╗   ██╗ ██████╗ ██████╗  █████╗ ███╗   ██╗
  ██╔══██╗╚██╗ ██╔╝██╔════╝ ██╔══██╗██╔══██╗████╗  ██║
  ██████╔╝ ╚████╔╝ ██║  ███╗██████╔╝███████║██╔██╗ ██║
  ██╔═══╝   ╚██╔╝  ██║   ██║██╔══██╗██╔══██║██║╚██╗██║
  ██║        ██║   ╚██████╔╝██║  ██║██║  ██║██║ ╚████║
  ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

  DEM simulation and analysis toolkit
  http://www.pygran.org, support@pygran.org
  Core developer and main author:
  Andrew Abi-Mansour, andrew.abi.mansour@pygran.org
  PyGran is open-source, distributed under the terms of the GNU Public
  License, version 2 or later. It is distributed in the hope that it will
  be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. You should have
  received a copy of the GNU General Public License along with PyGran.
  If not, see http://www.gnu.org/licenses . See also top-level README
  and LICENSE files.
'''

from setuptools import setup, find_packages
import os

# Extract metadata from simulation._version
with open(os.path.join('PyGranParams', '_version.py'), 'r') as fp:
	for line in fp.readlines():
		if '__version__' in line:
			__version__ = line.split('=')[-1].strip().strip("''")
		elif '__email__' in line:
			__email__ = line.split('=')[-1].strip().strip("''")
		elif '__author__' in line:
			__author__ = line.split('=')[-1].strip().strip("''")

setup(
	name = "PyGranParams",
	version = __version__,
	author = __author__,
	author_email = __email__,
	description = ("A PyGran submodule for materials definition"),
	license = "GNU v2",
	keywords = "Discrete Element Method, Granular Materials",
	url = "https://github.com/Andrew-AbiMansour/PyGranParams",
	packages = find_packages(),
	include_package_data = True,
	long_description = 'A PyGran submodule that serves as an extensible materials database. See http://www.pygran.org for more info on PyGran.',
	classifiers = [
			"Development Status :: 4 - Beta",
			"Topic :: Utilities",
			"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3.7",
			"Operating System :: POSIX :: Linux"
	],
	zip_safe = True
)

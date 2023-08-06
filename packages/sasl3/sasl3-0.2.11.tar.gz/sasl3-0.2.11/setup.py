#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.sysconfig import get_config_var
from distutils.version import LooseVersion
import os
import platform
from setuptools import setup, Extension
import sys

version = '0.2.11'

# From https://github.com/pandas-dev/pandas/pull/24274:
# For mac, ensure extensions are built for macos 10.9 when compiling on a
# 10.9 system or above, overriding distuitls behaviour which is to target
# the version that python was built for. This may be overridden by setting
# MACOSX_DEPLOYMENT_TARGET before calling setup.py
if sys.platform == 'darwin':
    if 'MACOSX_DEPLOYMENT_TARGET' not in os.environ:
        current_system = LooseVersion(platform.mac_ver()[0])
        python_target = LooseVersion(
            get_config_var('MACOSX_DEPLOYMENT_TARGET'))
        if python_target < '10.9' and current_system >= '10.9':
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'


sasl_module = Extension('sasl.saslwrapper',
                        sources=['sasl/saslwrapper.cpp'],
                        include_dirs=["sasl"],
                        libraries=["sasl2"],
                        language="c++")

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ''


setup(name='sasl3',
      version=version,
      url="http://github.com/sparkur/python-sasl3",
      maintainer="Ruslan Dautkhanov",
      maintainer_email="dautkhanov@gmail.com",
      description="""Cyrus-SASL bindings for Python""",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
      ],
      download_url="https://github.com/sparkur/python-sasl3/archive/v{}.tar.gz".format(version),
      packages=['sasl'],
      install_requires=['six'],
      ext_modules=[sasl_module],
      include_package_data=True
     )

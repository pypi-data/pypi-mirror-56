#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
#
# Ivy: a lightweight software bus
# Copyright (c) 2005-2019 Sébastien Bigaret <sebastien.bigaret@telecom-bretagne.eu>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of its copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY  THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS  OR IMPLIED WARRANTIES, INCLUDING, BUT  NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY  AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN  NO EVENT SHALL THE COPYRIGHT  OWNER OR CONTRIBUTORS BE
# LIABLE  FOR  ANY  DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,  EXEMPLARY,  OR
# CONSEQUENTIAL  DAMAGES  (INCLUDING,  BUT  NOT LIMITED  TO,  PROCUREMENT  OF
# SUBSTITUTE GOODS  OR SERVICES; LOSS OF  USE, DATA, OR  PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER  CAUSED AND  ON ANY THEORY  OF LIABILITY,  WHETHER IN
# CONTRACT,  STRICT LIABILITY,  OR TORT  (INCLUDING NEGLIGENCE  OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------------------------------------------

"""Ivy: a lightweight software bus

Ivy is a lightweight software bus for quick-prototyping protocols. It allows
applications to broadcast information through text messages, with a
subscription mechanism based on regular expressions.

It is compatible with both python 2.7+ and python 3.x.
"""
__version__="3.2"

#from distutils.core import setup
from setuptools import setup

# Instruction for PyPi found at:
# http://www.python.org/~jeremy/weblog/030924.html
classifiers = """\
Development Status :: 6 - Mature
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Natural Language :: English
Natural Language :: French
Topic :: Software Development :: Libraries :: Python Modules
"""

doclines = __doc__.split("\n")
short_description = doclines[0]
long_description = "\n".join(doclines[2:])

name = 'ivy-python'
version = __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name=name,
      version=version,
      license ="BSD License",
      description=short_description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Sébastien Bigaret",
      author_email="sebastien.bigaret@telecom-bretagne.eu",
      maintainer="Sebastien Bigaret",
      maintainer_email="sebastien.bigaret@telecom-bretagne.eu",
      url="http://www.eei.cena.fr/products/ivy/",
      project_urls={
          "Documentation": "https://ivy-python.readthedocs.io/",
          "Bug Tracker": "https://gitlab.com/ivybus/ivy-python/issues",
          "Source Code": "https://gitlab.com/ivybus/ivy-python/",
      },
      packages=['ivy', ],
      scripts=['examples/ivyprobe.py',],
      classifiers = list(filter(None, classifiers.split("\n"))),
)

# coding: UTF-8
'''Mock D-BUS objects for test suites.'''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.  See http://www.gnu.org/copyleft/lgpl.html for the full text
# of the license.

__author__ = 'Martin Pitt'
__email__ = 'martin.pitt@ubuntu.com'
__copyright__ = '(c) 2012 Canonical Ltd.'
__license__ = 'LGPL 3+'

from dbusmock.mockobject import DBusMockObject, MOCK_IFACE
from dbusmock.testcase import DBusTestCase

__all__ = ['DBusMockObject', 'MOCK_IFACE', 'DBusTestCase']

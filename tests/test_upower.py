#!/usr/bin/python3

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.  See http://www.gnu.org/copyleft/lgpl.html for the full text
# of the license.

__author__ = 'Martin Pitt'
__email__ = 'martin.pitt@ubuntu.com'
__copyright__ = '(c) 2012 Canonical Ltd.'
__license__ = 'LGPL 3+'

import unittest
import sys
import subprocess
import time

import dbus

import dbusmock


class TestUPower(dbusmock.DBusTestCase):
    '''Test mocking upowerd'''

    @classmethod
    def setUpClass(klass):
        klass.start_system_bus()
        klass.dbus_con = klass.get_dbus(True)

    def setUp(self):
        (self.p_mock, self.obj_upower) = self.spawn_server_template(
            'upower', {'OnBattery': True, 'HibernateAllowed': False}, stdout=subprocess.PIPE)
        self.dbusmock = dbus.Interface(self.obj_upower, dbusmock.MOCK_IFACE)

    def tearDown(self):
        self.p_mock.terminate()
        self.p_mock.wait()

    def test_no_devices(self):
        out = subprocess.check_output(['upower', '--dump'],
                                      universal_newlines=True)
        self.assertFalse('Device' in out, out)
        self.assertRegex(out, 'on-battery:\s+yes')
        self.assertRegex(out, 'lid-is-present:\s+yes')
        self.assertRegex(out, 'can-suspend:\s+yes')
        self.assertRegex(out, 'can-hibernate.*\sno')

    def test_one_ac(self):
        self.dbusmock.AddObject('/org/freedesktop/UPower/devices/mock_AC',
                                'org.freedesktop.UPower.Device',
                                {
                                    'PowerSupply': dbus.Boolean(True, variant_level=1),
                                    'Model': dbus.String('Mock AC', variant_level=1),
                                },
                                [])

        out = subprocess.check_output(['upower', '--dump'],
                                      universal_newlines=True)
        self.assertRegex(out, 'Device: /org/freedesktop/UPower/devices/mock_AC')
        self.assertRegex(out, 'on-battery:\s+yes')
        self.assertRegex(out, 'lid-is-present:\s+yes')
        #print('--------- out --------\n%s\n------------' % out)

        mon = subprocess.Popen(['upower', '--monitor-detail'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)

        time.sleep(0.3)
        self.dbusmock.EmitSignal('', 'DeviceChanged', 's',
                                 ['/org/freedesktop/UPower/devices/mock_AC'])
        time.sleep(0.2)

        mon.terminate()
        out = mon.communicate()[0]
        self.assertRegex(out, 'device changed:\s+/org/freedesktop/UPower/devices/mock_AC')
        #print('--------- monitor out --------\n%s\n------------' % out)

    def test_suspend(self):
        self.obj_upower.Suspend(dbus_interface='org.freedesktop.UPower')
        self.assertRegex(self.p_mock.stdout.readline(), b'^[0-9.]+ Suspend$')


if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))

"""
The ATEN PE switch component

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.aten-pe/
"""
import logging
from collections import namedtuple
from functools import lru_cache

import voluptuous as vol

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_HOST, CONF_NAME, CONF_PORT, CONF_USERNAME,
    STATE_ON, STATE_OFF, STATE_UNKNOWN)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pysnmp==4.4.4']

_LOGGER = logging.getLogger(__name__)

CONF_COMMUNITY = 'community'
CONF_AUTHKEY = 'authkey'
CONF_PRIVKEY = 'privkey'

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '161'
DEFAULT_COMMUNITY = 'private'
DEFAULT_USERNAME = 'administrator'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_COMMUNITY, default=DEFAULT_COMMUNITY): cv.string,
    vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): cv.string,
    vol.Required(CONF_AUTHKEY): cv.string,
    vol.Required(CONF_PRIVKEY): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the ATEN-PE switch."""
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    community = config.get(CONF_COMMUNITY)
    username = config.get(CONF_USERNAME)
    authkey = config.get(CONF_AUTHKEY)
    privkey = config.get(CONF_PRIVKEY)

    dev = AtenPE(node=host, serv=port, community=community,
                 username=username, authkey=authkey, privkey=privkey)

    switches = []
    for outlet in dev.outlets:
        switch = AtenSwitch(dev, outlet.id, outlet.name)
        switches.append(switch)

    add_devices(switches)
    return True


class AtenPE(object):
    _MIB_MODULE = 'ATEN-PE-CFG'
    _MIB_SRCURI = 'http://mibs.snmplabs.com/asn1/'

    def __init__(self, node, serv='snmp', community='private', username='administrator', authkey=None, privkey=None):
        self._prepareSnmpArgs(node, serv, community, username, authkey, privkey)
        self._prepareMibs()

    def _prepareSnmpArgs(self, node, serv, community, username, authkey, privkey):
        from pysnmp.hlapi import (
            CommunityData, ContextData, SnmpEngine, UdpTransportTarget,
            UsmUserData, usmAesCfb128Protocol, usmHMACMD5AuthProtocol)

        if authkey and privkey:
            self._snmp_args = [
                SnmpEngine(),
                UsmUserData(
                    username,
                    authkey,
                    privkey,
                    authProtocol=usmHMACMD5AuthProtocol,
                    privProtocol=usmAesCfb128Protocol,
                ),
                UdpTransportTarget((
                    node,
                    serv,
                )),
                ContextData()
            ]
        else:
             self._snmp_args = [
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((
                    node,
                    serv,
                )),
                ContextData()
            ]

    def _prepareMibs(self):
        from pysnmp.smi import builder, compiler
        mibBuilder = builder.MibBuilder()
        compiler.addMibCompiler(mibBuilder, sources=[self._MIB_SRCURI + '@mib@'])
        mibBuilder.loadModules(self._MIB_MODULE)

    def _set(self, objects_values, *args):
        from pysnmp.hlapi import (
            setCmd, ObjectIdentity, ObjectType)
        next(setCmd(
            *self._snmp_args,
            *[ObjectType(ObjectIdentity(self._MIB_MODULE, obj, *args), value) for obj, value in objects_values.items()]
        ))

    def _get(self, objects, *args):
        from pysnmp.hlapi import (
            getCmd, ObjectIdentity, ObjectType)
        return getCmd(
            *self._snmp_args,
            *[ObjectType(ObjectIdentity(self._MIB_MODULE, obj, *args)) for obj in objects]
        )

    def _next(self, objects, *args):
        from pysnmp.hlapi import (
            nextCmd, ObjectIdentity, ObjectType)
        return nextCmd(
            *self._snmp_args,
            *[ObjectType(ObjectIdentity(self._MIB_MODULE, obj, *args)) for obj in objects]
        )

    def _iterate(self, g):
        errorIndication, errorStatus, errorIndex, varBinds = next(g)
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            return [binds[1] for binds in varBinds]

        return []

    @property
    @lru_cache(maxsize=1)
    def _nrOutlets(self):
        return self._getAttribute('outletnumber')

    @property
    def _outletIDs(self):
        return range(1, self._nrOutlets + 1)

    @property
    def outlets(self):
        Outlet = namedtuple('outlet', ['id', 'name'])
        g = self._next(['outletName'])
        for n in self._outletIDs:
            name, = self._iterate(g)
            if not (name and name[0]):
                name = ''
            yield Outlet(n, str(name))

    def _getIndexedAttribute(self, name, index):
        s, = self._iterate(self._get([name], index))
        return s

    def _getAttribute(self, name):
        s, = self._iterate(self._next([name]))
        return s

    def _getNamedAttribute(self, name):
        s, = self._iterate(self._next([name]))
        return s.getNamedValues().getName(s)

    @property
    @lru_cache(maxsize=1)
    def deviceMAC(self):
        return str(self._getAttribute('deviceMAC'))

    def outletPower(self, outlet):
        return str(self._getIndexedAttribute('outletPower', outlet))

    def outletPowerDissipation(self, outlet):
        return str(self._getIndexedAttribute('outletPowerDissipation', outlet))

    def outletStatus(self, outlet):
        return str(self._getNamedAttribute('outlet%dStatus' % outlet))

    def setOutletStatus(self, outlet, state):
        self._set({ 'outlet%dStatus' % outlet: state }, 0)


class AtenSwitch(SwitchDevice):
    """Represents an ATEN-PE switch."""
    def __init__(self, device, outlet, name):
        self._device = device
        self._outlet = outlet
        self._name = name or 'Outlet %s' % outlet

    @property
    def should_poll(self):
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return True

    @property
    def unique_id(self):
        """Return a unique ID."""
        return '{mac}-{outlet}'.format(
            mac=self._device.deviceMAC,
            outlet=self._outlet
        )

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def state(self):
        """Return the state of the entity."""
        status = self._device.outletStatus(self._outlet)
        if status == 'on':
            return STATE_ON
        if status == 'off':
            return STATE_OFF
        return STATE_UNKNOWN

    @property
    def is_on(self):
        """Return True if entity is on."""
        return self._device.outletStatus(self._outlet) == 'on'

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.setOutletStatus(self._outlet, 'on')

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.setOutletStatus(self._outlet, 'off')

    def toggle(self, **kwargs):
        """Toggle the switch."""
        status = self._device.outletStatus(self._outlet)
        if status == 'on':
            self.turn_off(**kwargs)
        elif status == 'off':
            self.turn_on(**kwargs)

    @property
    def current_power_w(self):
         """Return the current power usage in W."""
         return self._device.outletPower(self._outlet)

    @property
    def today_energy_kwh(self):
         """Return the today total energy usage in kWh."""
         return self._device.outletPowerDissipation(self._outlet)

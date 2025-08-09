import unittest
from custom_components.eltako.sensor import *
from unittest import mock
from tests.mocks import *
from homeassistant.helpers.entity import Entity
from homeassistant.const import Platform
from custom_components.eltako.binary_sensor import EltakoBinarySensor
from eltakobus import *

# mock update of Home Assistant
Entity.schedule_update_ha_state = mock.Mock(return_value=None)
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestSensor_A5_10_03(unittest.TestCase):
    
    msg = Regular4BSMessage (address=b'\xFF\xFF\x00\x80', data=b'\x00\x80\x76\x00', status=0x00)

    def create_temp_sensor(self) -> EltakoTemperatureSensor:
        gateway = GatewayMock()
        dev_id = AddressExpression.parse("FF-FF-00-80")
        dev_name = "device name"
        dev_eep = EEP.find("A5-10-03")
        s = EltakoTemperatureSensor(Platform.SENSOR, gateway, dev_id, dev_name, dev_eep)
        return s
    
    def create_target_temp_sensor(self) -> EltakoTargetTemperatureSensor:
        gateway = GatewayMock()
        dev_id = AddressExpression.parse("FF-FF-00-80")
        dev_name = "device name"
        dev_eep = EEP.find("A5-10-03")
        s = EltakoTargetTemperatureSensor(Platform.SENSOR, gateway, dev_id, dev_name, dev_eep)
        return s
    
    def test_temp_sensor(self):
        ts = self.create_temp_sensor()

        self.assertEqual(ts.native_value, None)
        ts.value_changed(self.msg)

        print(A5_10_03.decode_message(self.msg).current_temperature)

        self.assertEqual(ts.native_value, 21.49019607843137)

    def test_target_temp_sensor(self):
        ts = self.create_target_temp_sensor()

        self.assertEqual(ts.native_value, None)
        ts.value_changed(self.msg)

        self.assertEqual(ts.native_value, 11)
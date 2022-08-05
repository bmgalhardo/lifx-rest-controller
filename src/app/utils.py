import lifxlan as lifx
from pydantic import BaseModel


class Device(BaseModel):
    ip: str
    mac: str


class DeviceName(Device):
    name: str


class Bulb(lifx.Light):

    def __init__(self, mac_addr, ip_addr):
        super().__init__(mac_addr, ip_addr)
        self._hue, self._saturation, self._brightness, self._kelvin = self.get_color()

    @property
    def state(self):
        return min(self.get_power(), 1)

    @property
    def hue(self):
        hue = self._hue / 65535 * 360
        return round(hue, 2)

    @property
    def saturation(self):
        """converts saturation to 0-1"""
        saturation = self._saturation / 65535
        return round(saturation, 2)

    @property
    def brightness(self):
        """converts brightness to 0-1"""
        brightness = self._brightness / 65535
        return round(brightness, 2)

    @property
    def kelvin(self):
        return self._kelvin


def get_all_devices() -> list[dict]:
    """
    Retrieve all devices in a given network
    :return: list of devices
    """
    devices: list[lifx.Light] = lifx.LifxLAN().get_lights()
    devices_found = {}

    if devices:
        try:
            devices_found = [{
                "ip": d.ip_addr,
                "mac": d.mac_addr,
                'label': d.get_label(),
                'group': d.get_group(),
            } for d in devices]
        except lifx.WorkflowException:
            pass

    return devices_found


def get_device_reading(mac: str, ip: str) -> dict:
    """
    Retrieve measurements of a given device
    :param mac: mac addr of device
    :param ip: ip of device
    :return: dictionary with the measurements
    """
    light = Bulb(mac, ip)
    light.refresh()
    data = {
        'state': light.state,
        'hue': light.hue,
        'saturation': light.saturation,
        'brightness': light.brightness,
        'kelvin': light.kelvin,
    }
    return data


def get_device_info(mac: str, ip: str) -> dict:
    """
    Get relevant info of a given bulb
    :param mac: mac addr of bulb
    :param ip: ip of bulb
    :return: dictionary with queried parameters
    """
    light = Bulb(mac, ip)
    light.refresh()
    data = {
        'ip': light.ip_addr,
        'mac': light.mac_addr,
        'port': light.port,
        'label': light.label,
        'group': light.group,
        'location': light.location,
        'state': light.state,
        'color': light.color,
        'hue': light.hue,
        'saturation': light.saturation,
        'brightness': light.brightness,
        'kelvin': light.kelvin,
        'product_name': light.product_name,
        'host_firmware_version': light.host_firmware_version,
        'wifi_firmware_version': light.wifi_firmware_version,
    }
    return data

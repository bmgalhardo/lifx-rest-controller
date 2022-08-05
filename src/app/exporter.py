import lifxlan as lifx
from prometheus_client import make_asgi_app, Gauge

from app.settings import Settings
from app.utils import get_device_reading

metrics_app = make_asgi_app()

bulb_state = Gauge(name='bulb_measurements_state',
                   documentation='Power state of light bulb',
                   labelnames=['group', 'location'])

bulb_hue = Gauge(name='bulb_measurements_hue',
                 documentation='Hue of light bulb',
                 labelnames=['group', 'location'])

bulb_saturation = Gauge(name='bulb_measurements_saturation',
                        documentation='Saturation of light bulb',
                        unit='percent',
                        labelnames=['group', 'location'])

bulb_brightness = Gauge(name='bulb_measurements_brightness',
                        documentation='Brightness of light bulb',
                        unit='percent',
                        labelnames=['group', 'location'])

bulb_kelvin = Gauge(name='bulb_measurements',
                    documentation='Colour temperature of light bulb',
                    unit='kelvin',
                    labelnames=['group', 'location'])


def update_metrics(settings: Settings) -> None:
    """
    Updates the prometheus metrics with the current measurements
    :param settings: configurations with the current device list
    """
    for device in settings.device_list:
        ip = device['ip']
        mac = device['mac']
        group = device['group']
        label = device['label']
        labels = [group, label]
        try:
            readings = get_device_reading(mac, ip)
            state = readings['state']
            hue = readings['hue']
            saturation = readings['saturation']
            brightness = readings['brightness']
            kelvin = readings['kelvin']
        except lifx.WorkflowException:
            state = 'nan'
            hue = 'nan'
            saturation = 'nan'
            brightness = 'nan'
            kelvin = 'nan'

        bulb_state.labels(*labels).set(state)
        bulb_hue.labels(*labels).set(hue)
        bulb_saturation.labels(*labels).set(saturation)
        bulb_brightness.labels(*labels).set(brightness)
        bulb_kelvin.labels(*labels).set(kelvin)

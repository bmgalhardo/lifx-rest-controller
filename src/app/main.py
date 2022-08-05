import uvicorn
import logging
import lifxlan as lifx

from fastapi import FastAPI, status, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.exporter import metrics_app, update_metrics
from app.settings import settings
from app.utils import get_all_devices, Device, get_device_info, get_device_reading, Bulb, DeviceName

app = FastAPI()
app.mount("/metrics", metrics_app)

logging.basicConfig(level=logging.INFO)


@app.get("/discover")
async def discover_devices():
    """
    Find all devices in the network through broadcast
    :return: list of devices
    """
    devices = get_all_devices()
    return devices


@app.post("/readings")
def get_info(device: Device):
    """
    Get smart device metrics
    :param device: device ip and mac addr
    :return: dictionary with the measurements
    """
    try:
        readings = get_device_reading(device.mac, device.ip)
        return readings
    except lifx.WorkflowException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/switch", status_code=status.HTTP_201_CREATED)
def toggle_switch(device: Device):
    """
    Toggle the power state of a given device. on->off OR off->on
    :param device: device ip and mac
    :return: current state of the device
    """
    light = Bulb(device.mac, device.ip)
    try:
        state = light.state

        if state:
            light.set_power(False)
            return {'on': False}
        else:
            light.set_power(True)
            return {'on': True}
    except lifx.WorkflowException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/label", status_code=status.HTTP_201_CREATED)
async def change_label(device_name: DeviceName):
    """
    Change the label of given device.
    This will be assigned to <location> in prometheus metrics
    :param device_name: device ip, mac addr and chosen name
    :return: device chosen name
    """
    light = Bulb(device_name.mac, device_name.ip)
    try:
        light.set_label(device_name.name)
        return {"name": device_name.name}
    except lifx.WorkflowException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/info")
def get_info(device: Device):
    """
    Retrieve device information
    :param device: device ip and mac addr
    :return: dictionary with relevant device info
    """
    try:
        info = get_device_info(device.mac, device.ip)
        return info
    except lifx.WorkflowException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.on_event("startup")
async def startup_event():
    """
    In server startup, start running the discovery and updates in parallel
    """
    logging.info('starting background tasks')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_metrics, 'interval', [settings], seconds=settings.update_period)
    scheduler.add_job(settings.update_device_list, 'interval', seconds=settings.discovery_period)
    scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from utils import dateConvert, validate
from .device import *
import hashlib
import datetime
import json
from collections import OrderedDict

class ProjectData:
    """
    @param{string|number} datetime - DateTime in string
    @param{string} project - Project Name
    @param{[Device]} devices - Device object
    @ param{number} totalEnergyUsage - TotalEnergyUsage
    @ param{number} averageRT - AverageRT
    @ param{string} geolocation - Geolocation
    """

    def __init__(self, dateTime, project_name, devices, totalEnergyUsage, averageRT, geolocation):
        self.project = project_name
        self.datetime = dateTime
        self.devices = devices
        self.totalEnergyUsage = totalEnergyUsage
        self.averageRT = averageRT
        self.geolocation = geolocation

        self.validate()
        self.datetime = dateConvert.formatdatetimestring(self.datetime)

    """
    @param {string} project - Project Name
    @param {string} datetime - DateTime in string
    @param {[Device]} devices - Device object
    @param {number} totalEnergyUsage - TotalEnergyUsage
    @param {number} averageRT - AverageRT
    @param {string} geolocation - Geolocation
    @returns {ProjectData}
    """

    @staticmethod
    def createWithCurrenTime(project_name, devices, totalEnergyUsage, averageRT, geolocation):

        currentDateTime = datetime.datetime.now()

        return ProjectData(currentDateTime, project_name, devices, totalEnergyUsage, averageRT, geolocation)

    def validate(self):
        if not isinstance(self.devices, list):
            raise Exception("devices ID is not an array")

        elif len(self.devices) == 0:
            raise Exception("devices cannot be empty")


        validate.number(self.averageRT, "AverageRT")
        validate.number(self.totalEnergyUsage, "TotalEnergyUsage")
        validate.string(self.geolocation, "Geolocation")
        validate.string(self.project, "Project")
        validate.datetimestring(self.datetime, "DateTime")


    def serializedDevice(self):
        serialized_Device = []

        for x in range(len(self.devices)):
            serialized_Device.append(self.devices[x].serialize())

        return serialized_Device


    def serialize(self):
        dataToSend = json.dumps(OrderedDict([("Project", self.project),
                                             ("DateTime", self.datetime),
                                             ("Devices", self.serializedDevice()),
                                             ("TotalEnergyUsage", self.totalEnergyUsage),
                                             ("AverageRT", self.averageRT),
                                             ("Geolocation", self.geolocation)]),
                                separators=(',', ':'))

        hash = hashlib.sha1((dataToSend).encode("utf-8")).hexdigest()
        print(hash)

        serialized = OrderedDict([
            ("data", dataToSend),
            ("checksum", hash)
        ])

        print(serialized)
        return serialized


options = {
    "limit": 5,
    "offset": 0,
    "start_date": "undefined",
    "end_date": "undefined"
}


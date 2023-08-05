from utils import validate


class Device:

    def __init__(self, deviceID, energyUsage):
        self.deviceID = deviceID
        self.energyUsage = energyUsage
        self.validate()

    def serialize(self):
        return {
            "DeviceId": self.deviceID,
            "EnergyUsage": self.energyUsage
        }

    def validate(self):
        validate.string(self.deviceID, "deviceId")
        validate.number(self.energyUsage, "energyUsage")



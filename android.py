from ppadb.client import Client as AdbClient
from ppadb.device import Device

class ADBMaster():
    def __init__(self):
        self.client = None

    def start(self, host = "127.0.0.1", port = 5037):
        try:
            self.client = AdbClient(host=host, port=port)
        except Exception as ex:
            print(ex)

    def printConnected(self):
        devices = self.client.devices()
        if len(devices) == 0:
            print("No connected devices found")
        else:
            for device in devices:
                print(f'Name: {device.get_properties()["ro.product.device"]} - Android {device.get_properties()["ro.build.version.release"]}')

    def isConnected(self, targetDevice : Device = None):
        if targetDevice is not None:
            output = targetDevice.shell("ping -c 1 google.com")
            if "bytes of data" in output:
                return True
            else:
                return False

    def isAirPlane(self, targetDevice: Device = None):
        if targetDevice is not None:
            output = targetDevice.shell("settings get global airplane_mode_on")
            if "0" in output:
                return False
            else:
                return True

    def toggleWifi(self, enable: bool, targetDevice : Device = None):
        command = "svc wifi enable" if enable else "svc wifi disable"
        if targetDevice is not None:
            targetDevice.shell(command)

    def toggleData(self, enable: bool, targetDevice : Device = None):
        command = "svc data enable" if enable else "svc data disable"
        if targetDevice is not None:
            targetDevice.shell(command)

    def toggleAirPlane(self, targetDevice : Device = None, enable : bool = False):
        if targetDevice is not None:
            output = targetDevice.shell("am start -a android.settings.AIRPLANE_MODE_SETTINGS ; sleep 0.1")
            if "Starting" in output:
                if enable:
                    targetDevice.shell("input keyevent 20 ; sleep 0.1")
                    targetDevice.shell("input keyevent 20")
                targetDevice.shell("input keyevent 23 ; sleep 0.1")
                if not enable:
                    targetDevice.shell("input keyevent 4")
                return True
            else:
                return False

    def browse(self, link, targetDevice: Device = None):
        if targetDevice is not None:
            targetDevice.shell(f"am start -n com.android.chrome/com.google.android.apps.chrome.Main -d '{link}'")
    
    def shellcmd(self, cmd, targetDevice : Device = None):
        if targetDevice is not None:
            targetDevice.shell(cmd)
        else:
            devices = self.client.devices()
            if len(devices) > 0:
                for device in devices:
                        device.shell(cmd)
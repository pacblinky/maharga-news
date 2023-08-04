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

    def toggleWifi(self, enable: bool, targetDevice : Device = None):
        command = "svc wifi enable" if enable else "svc wifi disable"
        if targetDevice is not None:
            targetDevice.shell(command)
        else:
            devices = self.client.devices()
            if len(devices) > 0:
                for device in devices:
                    device.shell(command)

    def toggleData(self, enable: bool, targetDevice : Device = None):
        command = "svc data enable" if enable else "svc data disable"
        if targetDevice is not None:
            targetDevice.shell(command)
        else:
            devices = self.client.devices()
            if len(devices) > 0:
                for device in devices:
                    device.shell(command)

    def toggleAirPlane(self, targetDevice : Device = None):
        if targetDevice is not None:
            targetDevice.shell("am start -a android.settings.AIRPLANE_MODE_SETTINGS")
            targetDevice.shell("input keyevent 20")
            targetDevice.shell("input keyevent 23")
            targetDevice.shell("input keyevent 4")
        else:
            devices = self.client.devices()
            if len(devices) > 0:
                for device in devices:
                    device.shell("am start -a android.settings.AIRPLANE_MODE_SETTINGS")
                    device.shell("input keyevent 20")
                    device.shell("input keyevent 23")
                    device.shell("input keyevent 4")
    
    def browse(self, link, targetDevice: Device = None):
        if targetDevice is not None:
            targetDevice.shell(f"am start -n com.android.chrome/org.chromium.chrome.browser.incognito.IncognitoTabLauncher \ -a android.intent.action.VIEW -d '{link}'")
        else:
            devices = self.client.devices()
            if len(devices) > 0:
                for device in devices:
                    device.shell(f"am start -n com.android.chrome/org.chromium.chrome.browser.incognito.IncognitoTabLauncher")
                    device.shell(f"am start -a android.intent.action.VIEW -d '{link}'")
    
    def shellcmd(self, cmd, targetDevice : Device = None):
        if targetDevice is not None:
            targetDevice.shell(cmd)
        else:
            devices = self.client.devices()
            if len(devices) > 0:
                for device in devices:
                        device.shell(cmd)

master = ADBMaster()
master.start()
master.printConnected()
master.browse("https://3d-sof2.com")
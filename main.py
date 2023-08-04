from android import ADBMaster
import tkinter as tk
import threading
import time
import random

loop = False

class DeviceThread(threading.Thread):
    def __init__(self, device, master : ADBMaster):
        threading.Thread.__init__(self)
        self.device = device
        self.master = master

    def run(self):
        global loop
        self.master.toggleWifi(False, self.device)
        self.master.toggleData(True, self.device)
        while loop:
            while True and loop == True:
                if self.master.isConnected(self.device):
                    break
            self.master.browse("https://3d-sof2.com", self.device)
            time.sleep(6)
            self.master.toggleAirPlane(self.device)
            while True and loop == True:
                if self.master.isAirPlane(self.device):
                    break
            self.master.toggleAirPlane(self.device)
                

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Maharga Views Bot')
        self.start_btn = tk.Button(self,text="Start", command=lambda:threading.Thread(target=self.start).start())
        self.close_btn = tk.Button(self,text="Stop", command=lambda:threading.Thread(target=self.stop).start(), state="disabled")
        self.start_btn.grid(row=0, column=0)
        self.close_btn.grid(row=1, column=0)
        self.threads = []

    def start(self):
        global loop
        loop = True
        master = ADBMaster()
        master.start()
        self.start_btn.configure(state="disabled")
        self.close_btn.configure(state="active")
        devices = master.client.devices()
        if len(devices) <= 0:
            print("No connected devices found")
        else:
            for device in devices:
                thread =  DeviceThread(device, master)
                self.threads.append(thread)
            for thready in self.threads:
                thready.start()
            print(f"Started with {len(self.threads)} devices")

    def stop(self):
        global loop
        loop = False
        self.start_btn.configure(state="active")
        self.close_btn.configure(state="disabled")
  
if __name__ == "__main__":
  app = App()
  app.mainloop()
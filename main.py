from android import ADBMaster
import tkinter as tk
import threading
import time
import random

class App(tk.Tk):
    def __init__(self):
        self.loop = False
        super().__init__()
        self.title('Maharga Views Bot')
        self.start_btn = tk.Button(self,text="Start", command=lambda:threading.Thread(target=self.start).start())
        self.close_btn = tk.Button(self,text="Stop", command=lambda:threading.Thread(target=self.stop).start(), state="disabled")
        self.start_btn.grid(row=0, column=0)
        self.close_btn.grid(row=1, column=0)

    def start(self):
        master = ADBMaster()
        master.start()
        self.start_btn.configure(state="disabled")
        self.close_btn.configure(state="active")
        self.loop = True
        master.toggleWifi(False)
        master.toggleData(True)
        while(self.loop):
            while(True and self.loop == True):
                if master.isConnected():
                    break
            master.browse("https://maharga.online")
            time.sleep(6)
            master.toggleAirPlane()
            master.toggleAirPlane()
            

    def stop(self):
        self.loop = False
        self.start_btn.configure(state="active")
        self.close_btn.configure(state="disabled")
  
if __name__ == "__main__":
  app = App()
  app.mainloop()
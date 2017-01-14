#!/usr/bin/env python

import Tkinter as tk
from Tkinter import N, S, E, W

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Tango Control System")

        # Handle closing the window with WM.
        master.protocol("WM_DELETE_WINDOW", self.quit)

        # Place window at the center of the screen.
        w = 500 # width for the Tk root
        h = 300 # height for the Tk root
        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        master.geometry("{}x{}+{}+{}".format(w, h, x, y))

        # Expand the main frame to root.
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=(N, S, E, W))

        # Variables of control system.
        self.devices = ["Camera", "Motor"]
        self.added_devices = ["Camera", "Motor"]
        self.attributes = ["Exposure Time", "Aperture", "Speed", "Step"]

        # Render the layout.
        self.create_widgets()

        # Tests
        raw_input("aaa")
        # self.update_menu(self.scannable_device_menu, self.selected_scannable_device, ["a", "b", "c", "d"])

    def update_menu(self, menu, variable, choices):
        """Update choices of OptionMenu."""
        variable.set('-')
        menu["menu"].delete(0, "end")
        for choice in choices:
            menu["menu"].add_command(label=choice, command=tk._setit(variable, choice))

    def create_widgets(self):
        """Widget."""
        # Scan.
        self.scan_frame = tk.LabelFrame(self, text="Scan")
        self.selected_scannable_device = tk.StringVar(self.scan_frame)
        self.selected_scannable_device.set("-")
        self.scannable_device_menu = tk.OptionMenu(self.scan_frame, self.selected_scannable_device, *self.added_devices)
        self.selected_scannable_attr = tk.StringVar(self.scan_frame)
        self.selected_scannable_attr.set("-")
        self.scannable_attr_menu = tk.OptionMenu(self.scan_frame, self.selected_scannable_attr, *self.attributes)
        self.add_scan_btn = tk.Button(self.scan_frame, text="Add")
        # Device.
        self.device_frame = tk.LabelFrame(self, text="Device")
        self.selected_device = tk.StringVar(self.device_frame)
        self.selected_device.set("-")
        self.device_menu = tk.OptionMenu(self.device_frame, self.selected_device, *self.devices)
        self.add_device_btn = tk.Button(self.device_frame, text="Add")

        """Grid."""
        # Main.
        self.scan_frame.grid(row=0, column=0, sticky=(N, S, E, W), padx=10, pady=10)
        self.device_frame.grid(row=1, column=0, sticky=(N, S, E, W), padx=10, pady=10)
        # Scan.
        self.scannable_device_menu.grid(row=0, column=0, sticky=(E, W))
        self.scannable_attr_menu.grid(row=0, column=1, sticky=(E, W))
        self.add_scan_btn.grid(row=0, column=2, sticky=(E, W), padx=10)
        # Device.
        self.device_menu.grid(row=1, column=0, sticky=(E, W))
        self.add_device_btn.grid(row=1, column=1, sticky=(E, W), padx=10)

        """Grid config."""
        # Main.
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        # Scan.
        self.scan_frame.columnconfigure(0, weight=3)
        self.scan_frame.columnconfigure(1, weight=3)
        self.scan_frame.columnconfigure(2, weight=1)
        # Device.
        self.device_frame.columnconfigure(0, weight=8)
        self.device_frame.columnconfigure(1, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

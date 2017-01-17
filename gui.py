#!/usr/bin/env python

import Tkinter as tk
from Tkinter import N, S, E, W

import widget

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Variables of control system.
        self.devices_type = ["Camera", "Motor"]
        self.devices_name = ["PointGrey", "Dummy_motor"]
        self.added_devices = ["PointGrey", "Dummy_motor"]
        self.attributes = ["Exposure Time", "Aperture", "Speed", "Step"]
        self.scan_entries = []
        self.device_entries = []

        # Render the layout.
        self.configure_master()
        self.create_widgets()

        # Tests
        # raw_input("aaa")
        # self.update_menu(self.scannable_device_menu, self.selected_scannable_device, ["a", "b", "c", "d"])

    def configure_master(self):
        # Set window title.
        self.master.title("Tango Control System")

        # Handle closing the window with window manager.
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        # Place window at the center of the screen.
        w = 500 # Width for the Tk root.
        h = 300 # Height for the Tk root.
        ws = self.master.winfo_screenwidth() # Width of the screen.
        hs = self.master.winfo_screenheight() # Height of the screen.
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry("{}x{}+{}+{}".format(w, h, x, y))

        # Expand the main frame to root.
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=(N, S, E, W))

    """Widget helper methods."""
    def update_menu(self, menu, variable, choices):
        """Update choices of OptionMenu."""
        variable.set('-')
        menu["menu"].delete(0, "end")
        for choice in choices:
            menu["menu"].add_command(label=choice, command=tk._setit(variable, choice))

    def open_log_setting(self):
        # TODO.
        log_setting_win = tk.Toplevel(self.master)

    def open_tutorial(self):
        # TODO.
        tutorial_win = tk.Toplevel(self.master)

    def open_about(self):
        # TODO.
        about_win = tk.Toplevel(self.master)

    def start_scan(self):
        # TODO.
        pass

    def stop_scan(self):
        # TODO.
        pass

    def add_scan(self):
        device = self.selected_scannable_device.get()
        attr = self.selected_scannable_attr.get()
        # Avoid unspecified device or attr.
        if device == "-" or attr == "-":
            return
        entry = widget.ScanEntry(self.scan_frame, device, attr)
        self.scan_entries.append(entry)
        entry.grid(row=len(self.scan_entries)+1, column=0, columnspan=3, sticky=(E, W), padx=11, pady=3)

    def add_device(self):
        device_name = self.selected_device.get()
        # Avoid unspecified device.
        if device_name == "-":
            return
        device_type = self.devices_type[self.devices_name.index(device_name)]
        device = getattr(widget, device_type + "Device")(self.device_workspace_frame, device_name)
        self.device_entries.append(device)
        device.grid(row=0, column=len(self.device_entries), sticky=(N, S), padx=5)
        self.added_devices.append(device_name)

    def create_widgets(self):
        """Widget."""
        # Menu.
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.setting_menu = tk.Menu(self.menubar, tearoff=0)
        self.setting_menu.add_command(label="Log", command=self.open_log_setting)
        self.setting_menu.add_separator()
        self.setting_menu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Setting", menu=self.setting_menu)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Tutorial", command=self.open_tutorial)
        self.help_menu.add_command(label="About", command=self.open_about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # TODO: scrollbar
        # Scan.
        self.scan_frame = tk.LabelFrame(self, text="Scan")
        self.scan_start_btn = tk.Button(self.scan_frame, text="Start", fg="white", bg="blue", command=self.start_scan)
        self.scan_stop_btn = tk.Button(self.scan_frame, text="Stop", fg="white", bg="red", command=self.stop_scan)
        self.selected_scannable_device = tk.StringVar(self.scan_frame)
        self.selected_scannable_device.set("-")
        self.scannable_device_menu = tk.OptionMenu(self.scan_frame, self.selected_scannable_device, *self.added_devices)
        self.selected_scannable_attr = tk.StringVar(self.scan_frame)
        self.selected_scannable_attr.set("-")
        self.scannable_attr_menu = tk.OptionMenu(self.scan_frame, self.selected_scannable_attr, *self.attributes)
        self.add_scan_btn = tk.Button(self.scan_frame, text="Add", command=self.add_scan)
        # Device.
        self.device_frame = tk.LabelFrame(self, text="Device")
        self.selected_device = tk.StringVar(self.device_frame)
        self.selected_device.set("-")
        self.device_menu = tk.OptionMenu(self.device_frame, self.selected_device, *self.devices_name)
        self.add_device_btn = tk.Button(self.device_frame, text="Add", command=self.add_device)
        self.device_workspace_frame = tk.Frame(self.device_frame)

        """Grid."""
        # Main.
        self.scan_frame.grid(row=0, column=0, sticky=(N, S, E, W), padx=10, pady=10)
        self.device_frame.grid(row=1, column=0, sticky=(N, S, E, W), padx=10, pady=10)
        # Scan.
        self.scan_start_btn.grid(row=0, column=0, columnspan=2, sticky=(E, W), padx=(10,5))
        self.scan_stop_btn.grid(row=0, column=2, sticky=(E, W), padx=(5,10))
        self.scannable_device_menu.grid(row=1, column=0, sticky=(E, W), padx=(7,0))
        self.scannable_attr_menu.grid(row=1, column=1, sticky=(E, W), padx=(3,4))
        self.add_scan_btn.grid(row=1, column=2, sticky=(E, W), padx=(5,10))
        # Device.
        self.device_menu.grid(row=0, column=0, sticky=(E, W), padx=(7,0))
        self.add_device_btn.grid(row=0, column=1, sticky=(E, W), padx=(9,10))
        self.device_workspace_frame.grid(row=1, column=0, columnspan=2, sticky=(N, S, E, W), padx=10, pady=(3,8))

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
        self.device_frame.rowconfigure(1, weight=1)
        self.device_frame.columnconfigure(0, weight=4)
        self.device_frame.columnconfigure(1, weight=1)
        self.device_workspace_frame.rowconfigure(0, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

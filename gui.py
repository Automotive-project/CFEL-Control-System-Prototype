#!/usr/bin/env python
# pylint: disable=attribute-defined-outside-init, fixme, too-many-instance-attributes, too-many-public-methods, unused-variable
"""This module is the main GUI for Control System.

Tkinter is used for GUI.

"""

import Tkinter as tk
from Tkinter import N, S, E, W

import widget

class Application(tk.Frame):
    """Main class for GUI.

    This frame is the only child of the root container. Besides the top menubar,
    it has two children. The |scan_frame| is for scanning, and the
    |device_frame| is for device.

    Attributes:
        TODO

    """
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Variables of control system.
        self.devices_type = ["Camera", "Camera", "Motor", "Motor"]
        self.devices_name = ["PointGrey1",
                             "PointGrey2",
                             "Dummy_motor1",
                             "Dummy_motor2"]
        self.added_devices = []
        self.attributes = ["Exposure Time", "Aperture", "Speed", "Step"]

        # Render the layout.
        self._configure_master()
        self._create_widgets()

        # Tests
        # raw_input("aaa")
        # self.update_menu(self.scannable_device_menu,
                # self.selected_scannable_device, self.added_devices)

    def _add_device(self):
        """Add device entry.

        Triggered by |add_device_btn|.

        """
        device_name = self.selected_device.get()
        # Avoid unspecified device.
        if device_name == "-":
            return
        # TODO: remove device from |devices_name| after being added.
        # TODO: maintain order of |devices_name|.
        # TODO: maintain |added_devices| and |devices_name| in device.on_destroy
        device_type = self.devices_type[self.devices_name.index(device_name)]
        device = getattr(widget, device_type + "Device") \
                (self.device_workspace_frame, device_name)
        device.grid(row=0, column=len(self.device_workspace_frame.children),
                    sticky=(N, S), padx=5)
        self.added_devices.append(device_name)
        self._update_menu(self.scannable_device_menu,
                          self.selected_scannable_device, self.added_devices)
        print len(self.added_devices)
        print self.device_workspace_frame.children

    def _add_scan(self):
        """Add scan entry.

        Triggered by |add_scan_btn|.

        """
        device = self.selected_scannable_device.get()
        attr = self.selected_scannable_attr.get()
        # Avoid unspecified device or attr.
        if device == "-" or attr == "-":
            return
        entry = widget.ScanEntry(self.scan_workspace_frame, device, attr)
        entry.grid(row=len(self.scan_workspace_frame.children), column=0,
                   sticky=(E, W), pady=3)

    def _configure_master(self):
        """Configure the root container.

        Includes title, closing event, start position and grid.

        """
        # Set window title.
        self.master.title("Tango Control System")

        # Handle closing the window with window manager.
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        # Place window at the center of the screen.
        width = 800 # Width for the Tk root.
        height = 600 # Height for the Tk root.
        screen_width = self.master.winfo_screenwidth() # Width of the screen.
        screen_height = self.master.winfo_screenheight() # Height of the screen.
        pos_x = (screen_width/2) - (width/2)
        pos_y = (screen_height/2) - (height/2)
        self.master.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))

        # Expand the main frame to root.
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=(N, S, E, W))

    def _create_widgets(self):
        """Create and configure all widgets."""
        # Menu.
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.setting_menu = tk.Menu(self.menubar, tearoff=0)
        self.setting_menu.add_command(label="Log",
                                      command=self._open_log_setting)
        self.setting_menu.add_separator()
        self.setting_menu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Setting", menu=self.setting_menu)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Tutorial",
                                   command=self._open_tutorial)
        self.help_menu.add_command(label="About", command=self._open_about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # TODO: scrollbar
        # Scan.
        self.scan_frame = tk.LabelFrame(self, text="Scan")
        self.scan_start_btn = tk.Button(self.scan_frame, text="Start",
                                        fg="white", bg="blue",
                                        command=self._start_scan)
        self.scan_stop_btn = tk.Button(self.scan_frame, text="Stop", fg="white",
                                       bg="red", command=self._stop_scan)
        self.selected_scannable_device = tk.StringVar(self.scan_frame, "-")
        self.scannable_device_menu = \
                tk.OptionMenu(self.scan_frame, self.selected_scannable_device,
                              "-", command=self._on_scannable_device_change)
        # TODO: update |scannable_attr_menu| -> |scannable_device_menu| changed.
        self.selected_scannable_attr = tk.StringVar(self.scan_frame, "-")
        self.scannable_attr_menu = tk.OptionMenu(self.scan_frame,
                                                 self.selected_scannable_attr,
                                                 "-")
        self.add_scan_btn = tk.Button(self.scan_frame, text="Add",
                                      command=self._add_scan)
        self.scan_workspace_frame = tk.Frame(self.scan_frame)
        # Device.
        self.device_frame = tk.LabelFrame(self, text="Device")
        self.selected_device = tk.StringVar(self.device_frame, "-")
        self.device_menu = tk.OptionMenu(self.device_frame,
                                         self.selected_device,
                                         *self.devices_name)
        self.add_device_btn = tk.Button(self.device_frame, text="Add",
                                        command=self._add_device)
        self.device_workspace_frame = tk.Frame(self.device_frame)

        # Grid.
        # Scan.
        self.scan_frame.grid(row=0, column=0, sticky=(N, S, E, W),
                             padx=10, pady=10)
        self.scan_start_btn.grid(row=0, column=0, columnspan=2, sticky=(E, W),
                                 padx=(10, 5))
        self.scan_stop_btn.grid(row=0, column=2, sticky=(E, W), padx=(5, 10))
        self.scannable_device_menu.grid(row=1, column=0, sticky=(E, W),
                                        padx=(7, 0))
        self.scannable_attr_menu.grid(row=1, column=1, sticky=(E, W),
                                      padx=(3, 4))
        self.add_scan_btn.grid(row=1, column=2, sticky=(E, W), padx=(5, 10))
        self.scan_workspace_frame.grid(row=2, column=0, columnspan=3,
                                       sticky=(N, S, E, W), padx=11)
        # Device.
        self.device_frame.grid(row=1, column=0, sticky=(N, S, E, W),
                               padx=10, pady=10)
        self.device_menu.grid(row=0, column=0, sticky=(E, W), padx=(7, 0))
        self.add_device_btn.grid(row=0, column=1, sticky=(E, W), padx=(9, 10))
        self.device_workspace_frame.grid(row=1, column=0,
                                         columnspan=2, sticky=(N, S, E, W),
                                         padx=10, pady=(3, 8))

        # Grid config.
        # Main.
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        # Scan.
        self.scan_frame.columnconfigure(0, weight=3)
        self.scan_frame.columnconfigure(1, weight=3)
        self.scan_frame.columnconfigure(2, weight=1)
        self.scan_workspace_frame.columnconfigure(0, weight=1)
        # Device.
        self.device_frame.rowconfigure(1, weight=1)
        self.device_frame.columnconfigure(0, weight=4)
        self.device_frame.columnconfigure(1, weight=1)
        self.device_workspace_frame.rowconfigure(0, weight=1)

    def _on_scannable_device_change(self, device):
        """On |scannable_device_menu| change."""
        # TODO.
        pass

    def _open_about(self):
        """Open about menu."""
        # TODO.
        about_win = tk.Toplevel(self.master)

    def _open_log_setting(self):
        """Open log setting menu."""
        # TODO.
        log_setting_win = tk.Toplevel(self.master)

    def _open_tutorial(self):
        """Open tutorial menu."""
        # TODO.
        tutorial_win = tk.Toplevel(self.master)

    def _start_scan(self):
        """Start scanning."""
        # TODO.
        pass

    def _stop_scan(self):
        """Stop scanning."""
        # TODO.
        pass

    @staticmethod
    def _update_menu(menu, variable, choices):
        """Update choices of OptionMenu."""
        variable.set("-")
        menu["menu"].delete(0, "end")
        for choice in choices if choices else ["-"]:
            menu["menu"].add_command(label=choice,
                                     command=lambda c=choice: variable.set(c))


if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = Application(master=ROOT)
    APP.mainloop()
    ROOT.destroy()

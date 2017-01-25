#!/usr/bin/env python
# pylint: disable=attribute-defined-outside-init, fixme, line-too-long, too-few-public-methods, too-many-instance-attributes, too-many-public-methods, unused-variable
"""This module is the main GUI for Control System.

Tkinter is used for GUI.

"""

from collections import deque

import Tkinter as tk
from Tkinter import N, S, E, W

import PyTango

import widget

class Tango(object):
    """Data class. Interact with tango system."""
    def __init__(self):
        self._db = PyTango.Database()

        self.device_classes = ["Motor", "LimaCCDs"]
        self.devices = []
        for class_type in self.device_classes:
            self.devices.extend(self._db.get_device_exported_for_class(class_type).value_string)

    def get_device_class(self, device):
        """Return the tango class of |device|."""
        return self._db.get_class_for_device(device)


class Application(tk.Frame):
    """Main class for GUI.

    This frame is the only child of the root container. Besides the top menubar,
    it has two children. The |scan_frame| is for scanning, and the
    |device_frame| is for device management.

    Args:
        master (tk.Widget): reference to parent widget.

    Attributes:
        tango (Tango): tango control system interface.
        devices (list of str): name of available devices, excluding added ones.
        added_devices (list of str): name of added devices.

    """
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Load data from tango.
        self.tango = Tango()
        self.devices = sorted(self.tango.devices)
        self.added_devices = []

        # Render the layout.
        self._configure_master()
        self._create_widgets()

    def _add_device(self):
        """Add device entry.

        Triggered by |add_device_btn|. Maintain lists |devices| and
        |added_devices|, menus |device_menu| and |scannable_device_menu| as well.

        """
        device_name = self.selected_device.get()
        # Avoid unspecified device.
        if device_name == "-":
            return
        device_class = self.tango.get_device_class(device_name)
        device = getattr(widget, device_class + "Device") \
                (self, self.device_workspace_frame, device_name)
        device.grid(row=0, column=len(self.device_workspace_frame.children),
                    sticky=(N, S), padx=5)
        self.added_devices.append(device_name)
        self._update_menu(self.scannable_device_menu,
                          self.selected_scannable_device, self.added_devices)
        self.devices.remove(device_name)
        self._update_menu(self.device_menu, self.selected_device, self.devices)

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

        # Make all widgets focusable in order to remove focus from widget, like
        # entry, when clicking elsewhere.
        self.bind_all("<1>", lambda event:event.widget.focus_set())

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
        self.selected_scannable_device.trace("w", self._on_scannable_device_change)
        self.scannable_device_menu = \
                tk.OptionMenu(self.scan_frame, self.selected_scannable_device,
                              "-", command=self._on_scannable_device_change)
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
                                         *self.devices)
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

    def _on_scannable_device_change(self, *args):
        """On |scannable_device_menu| change.

        Maintain |scannable_attr_menu|.
        """
        device_name = self.selected_scannable_device.get()
        if device_name == "-":
            self._update_menu(self.scannable_attr_menu,
                              self.selected_scannable_attr, [])
            return
        device = self.device_workspace_frame.children[device_name.lower()]
        attributes = []
        # FIX: Is |common_attr| == scannable_attr?
        for attr in device.common_attr:
            attributes.append(attr.name)
        self._update_menu(self.scannable_attr_menu,
                          self.selected_scannable_attr, attributes)

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

    def _remove_device(self, device):
        """Remove device entry.

        Triggered by |widget.DeviceBase.delete_btn|. Maintain lists |devices|
        and |added_devices|, menus |device_menu| and |scannable_device_menu| as
        well. Also, remove scan entries related to device.

        """
        self.added_devices.remove(device)
        self._update_menu(self.scannable_device_menu,
                          self.selected_scannable_device, self.added_devices)
        self.devices.append(device)
        list.sort(self.devices)
        self._update_menu(self.device_menu, self.selected_device, self.devices)

        for entry in self.scan_workspace_frame.children.values():
            if entry.device == device:
                entry.destroy()

    def _start_scan(self):
        """Start scanning."""
        # TODO.
        self.change_state(self, False)
        self.change_state(self.scan_stop_btn, True)

    def _stop_scan(self):
        """Stop scanning."""
        # TODO.
        self.change_state(self, True)
        for entry in self.scan_workspace_frame.children.values():
            entry.update_state()

    @staticmethod
    def _update_menu(menu, variable, choices):
        """Update choices of OptionMenu.

        Args:
            menu (tk.Optionmenu): menu to be updated.
            variable (tk.Variable): variable bound with |menu|.
            choices (list of str): new options to be assigned to |menu|.

        """
        variable.set("-")
        menu["menu"].delete(0, "end")
        for choice in choices if choices else ["-"]:
            menu["menu"].add_command(label=choice,
                                     command=lambda c=choice: variable.set(c))

    @staticmethod
    def change_state(widget, state):
        """Change |widget| to state enabled or disabled, and all its children
        recursively.

        Args:
            widget (tk.Widget): widget to be changed.
            state (bool): enable or disable the |widget|.

        """
        if state:
            # State config for widget label.
            label_cfg = {"fg": "black"}
            # State config for other widgets, including button, checkbutton,
            # entry, optionmenu.
            cfg = {"state": tk.NORMAL}
        else:
            label_cfg = {"fg": "grey"}
            cfg = {"state": tk.DISABLED}
        widgets = deque([widget])
        while widgets:
            w = widgets.popleft()
            widgets.extend(w.children.values())
            if w.widgetName == "label":
                w.config(**label_cfg)
            elif w.widgetName in ["button", "checkbutton", "entry",
                                  "menubutton"]:
                w.config(**cfg)


if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = Application(master=ROOT)
    APP.mainloop()
    ROOT.destroy()

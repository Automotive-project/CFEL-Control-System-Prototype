#!/usr/bin/env python
# pylint: disable=attribute-defined-outside-init, fixme, no-self-use, too-few-public-methods, too-many-ancestors, too-many-instance-attributes, too-many-public-methods, unused-variable
"""This module contains custom widgets for Control System GUI.

Tkinter is used for GUI.

"""

import Tkinter as tk
from Tkinter import N, S, E, W

# TODO: Maybe a dict or a namedtuple will be a better choice?
class Attribute(object):
    """Helper class for device attribute.

    Args:
        name (str): attribute name.
        w_type (tk.Widget): type of the value widget.

    Attributes:
        name (str): attribute name.
        widget_type (tk.Widget): type of the |value_widget|.
        name_widget: reference to name widget.
        value_widget: reference to value widget.

    """
    def __init__(self, name="ATTR_NAME", w_type=None):
        self.name = name
        self.widget_type = w_type
        self.name_widget = None
        self.value_widget = None


class DeviceBase(tk.Frame):
    """Base class of device widget.

    Derived classed should follow the naming convention: TypeDevice, eg.
    CameraDevice, and define its own attributes at initialization followed by
    a call of _create_widgets().

    Attributes:
        device_type (str): type of device, eg. Camera.
        device_name (str): name of device, eg. cfeld/limaccds/poingrey
        common_attr (list of |Attribute|): common attributes.
        other_attr (list of |Attribute|):
                other attributes displayed only in expert mode.

    """
    def __init__(self, master):
        tk.Frame.__init__(self, master, borderwidth=2, relief=tk.RAISED)

        self.device_type = ""
        self.device_name = ""
        self.common_attr = []
        self.other_attr = []

    def _create_widgets(self):
        """Create and configure all widgets."""
        # Header.
        self.header_frame = tk.Frame(self)
        self.device_label = tk.Label(self.header_frame, text=self.device_name,
                                     font="-weight bold")
        self.is_expert = tk.IntVar(self, 0)
        self.expert_chkbtn = tk.Checkbutton(self.header_frame,
                                            variable=self.is_expert,
                                            command=self._toggle_expert)
        # Body.
        self.common_attr_frame = tk.Frame(self)
        self.other_attr_frame = tk.Frame(self)
        for attr in self.common_attr:
            attr.name_widget = tk.Label(self.common_attr_frame, text=attr.name)
            attr.value_widget = \
                    attr.widget_type(self.common_attr_frame, width=10)
        for attr in self.other_attr:
            attr.name_widget = tk.Label(self.other_attr_frame, text=attr.name)
            attr.value_widget = \
                    attr.widget_type(self.other_attr_frame, width=10)
        # Footer.
        self.delete_btn = tk.Button(self, text="Delete", font="-weight bold",
                                    fg="white", bg="red", command=self._delete)

        # Grid.
        # Header.
        self.header_frame.grid(row=0, column=0, sticky=(E, W),
                               padx=(5, 5), pady=(5, 5))
        self.device_label.grid(row=0, column=0, sticky=(E, W))
        self.expert_chkbtn.grid(row=0, column=1)
        # Body.
        self.common_attr_frame.grid(row=1, column=0, sticky=(N, S, E, W),
                                    padx=(5, 5))
        for idx, attr in enumerate(self.common_attr):
            attr.name_widget.grid(row=idx, column=0, sticky=(W), padx=(0, 5))
            attr.value_widget.grid(row=idx, column=1, sticky=(E, W))
        self.other_attr_frame.grid(row=2, column=0, sticky=(N, S, E, W),
                                   padx=(5, 5))
        self.other_attr_frame.grid_remove()
        for idx, attr in enumerate(self.other_attr):
            attr.name_widget.grid(row=idx, column=0, sticky=(W), padx=(0, 5))
            attr.value_widget.grid(row=idx, column=1, sticky=(E, W))
        # Footer.
        self.delete_btn.grid(row=3, column=0, sticky=(E, W), padx=(5, 5))

        # Grid config.
        # Main.
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        # Header.
        self.header_frame.columnconfigure(0, weight=1)
        # Body.
        self.common_attr_frame.columnconfigure(0, weight=1)
        self.common_attr_frame.columnconfigure(1, weight=1)
        self.other_attr_frame.columnconfigure(0, weight=1)
        self.other_attr_frame.columnconfigure(1, weight=1)

    def _delete(self):
        """Delete widget."""
        self.destroy()
        # TODO: delete from |Application.added_devices|.

    def _toggle_expert(self):
        """Toggle expert mode. Bound with |expert_chkbtn|."""
        if self.is_expert.get() == 0:
            self.other_attr_frame.grid_remove()
        else:
            self.other_attr_frame.grid()


class CameraDevice(DeviceBase):
    """Device widget of Camera.

    Common attributes:
        - Exposure time: tk.Entry

    Other attributes:
        - Aperture: tk.Entry

    """
    def __init__(self, master, name):
        DeviceBase.__init__(self, master)

        self.device_type = "Camera"
        self.device_name = name
        self.common_attr = [Attribute("Exposure Time", tk.Entry)]
        self.other_attr = [Attribute("Aperture", tk.Entry)]

        self._create_widgets()


class ScanEntry(tk.Frame):
    """Scan widget for a single attribute.

    Args:
        device (str): device to be scanned.
        attr (str): attribute to be scanned.

    """
    def __init__(self, master, device, attr):
        tk.Frame.__init__(self, master, borderwidth=2, relief=tk.RAISED)

        self._create_widgets(device, attr)

    def _create_widgets(self, device, attr):
        """Create and configure all widgets."""
        # Accessibility.
        self.enabled = tk.IntVar(self, 1)
        self.state_chkbtn = tk.Checkbutton(self, variable=self.enabled,
                                           command=self._toggle_state)
        # Device and attributes.
        self.device_attr_label = tk.Label(self, text=device + "::" + attr)
        # Start, end, step.
        entry_width = 15
        self.start_entry = tk.Entry(self, fg="grey", width=entry_width)
        self.start_entry.insert(0, "start")
        self.start_entry.bind("<FocusIn>", self._on_entry_focusin)
        self.start_entry.bind("<FocusOut>", self._on_entry_focusout)
        self.end_entry = tk.Entry(self, fg="grey", width=entry_width)
        self.end_entry.insert(0, "end")
        self.end_entry.bind("<FocusIn>", self._on_entry_focusin)
        self.end_entry.bind("<FocusOut>", self._on_entry_focusout)
        self.step_entry = tk.Entry(self, fg="grey", width=entry_width)
        self.step_entry.insert(0, "step")
        self.step_entry.bind("<FocusIn>", self._on_entry_focusin)
        self.step_entry.bind("<FocusOut>", self._on_entry_focusout)
        # Delete.
        self.delete_btn = tk.Button(self, text="X", font="-weight bold",
                                    fg="white", bg="red", width=1,
                                    command=self._delete)

        self.columnconfigure(1, weight=1)
        self.state_chkbtn.grid(row=0, column=0)
        self.device_attr_label.grid(row=0, column=1, sticky=(W))
        self.start_entry.grid(row=0, column=2)
        self.end_entry.grid(row=0, column=3)
        self.step_entry.grid(row=0, column=4)
        self.delete_btn.grid(row=0, column=5)

    def _delete(self):
        """Delete widget."""
        self.destroy()
        # TODO: delete from |Application.scan_entries|.

    def _on_entry_focusin(self, event):
        """On tk.entry is focused. Bound with event <FocusIn>.

        Remove hint in the entry.

        """
        if event.widget.get() in ["start", "end", "step"]:
            event.widget.delete(0, "end")
            event.widget.config(fg="black")

    def _on_entry_focusout(self, event):
        """On tk.entry is not focused. Bound with event <FocusOut>.

        Add hint to the entry if empty.

        """
        if event.widget.get():
            return
        event.widget.config(fg="grey")
        if event.widget == self.start_entry:
            event.widget.insert(0, "start")
        elif event.widget == self.end_entry:
            event.widget.insert(0, "end")
        elif event.widget == self.step_entry:
            event.widget.insert(0, "step")

    def _toggle_state(self):
        """Toggle between enabled and disabled. Bound with |state_chkbtn|."""
        if self.enabled.get() == 0:
            self.device_attr_label.config(fg="grey")
            self.start_entry.config(state=tk.DISABLED)
            self.end_entry.config(state=tk.DISABLED)
            self.step_entry.config(state=tk.DISABLED)
        else:
            self.device_attr_label.config(fg="black")
            self.start_entry.config(state=tk.NORMAL)
            self.end_entry.config(state=tk.NORMAL)
            self.step_entry.config(state=tk.NORMAL)


if __name__ == "__main__":
    ROOT = tk.Tk()
    ATTR = Attribute("TEST_ATTR")
    CAMERA = CameraDevice(ROOT, "TEST_CAMERA")
    ENTRY = ScanEntry(ROOT, "TEST_DEVICE", "TEST_ATTR")
    ROOT.destroy()

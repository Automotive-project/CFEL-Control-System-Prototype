#!/usr/bin/env python
# pylint: disable=attribute-defined-outside-init, fixme, no-self-use, too-few-public-methods, too-many-ancestors, too-many-instance-attributes, too-many-public-methods, unused-variable
"""This module contains custom widgets for Control System GUI.

Tkinter is used for GUI.

"""

import os
import time
import Tkinter as tk
from Tkinter import N, S, E, W

import PyTango

import gui

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

    Device widget is created with option name and lower-case |name| as value in
    order to retrieve the widget reference by device name from dict
    |device_workspace_frame.children|.

    Args:
        app: reference to main frame.
        master: reference to parent widget.
        name (str): device name.

    Attributes:
        device_type (str): type of device, eg. Camera.
        device_name (str): name of device, eg. cfeld/limaccds/poingrey.
        tango_device: instance of tango device proxy.
        is_always_recording (bool): whether record device info when scanning.
        common_attr (list of |Attribute|): common attributes.
        other_attr (list of |Attribute|):
                other attributes which are displayed only in expert mode.

    """
    def __init__(self, app, master, name):
        tk.Frame.__init__(self, master, name=name.lower(), borderwidth=2,
                          relief=tk.RAISED)

        self.app = app
        self.device_type = "DeviceBase"
        self.device_name = name
        self.tango_device = PyTango.DeviceProxy(name)
        self.is_always_log = False
        self.common_attr = []
        self.scannable_attr = []
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
                                            command=self._update_mode)
        # Body.
        self.common_attr_frame = tk.Frame(self)
        self.other_attr_frame = tk.Frame(self)
        for attr in self.common_attr:
            attr.name_widget = tk.Label(self.common_attr_frame, text=attr.name)
            attr.value_widget = \
                    attr.widget_type(self.common_attr_frame, width=10)
            attr.value_widget.insert(0, self.get_attribute(attr.name))
        for attr in self.other_attr:
            attr.name_widget = tk.Label(self.other_attr_frame, text=attr.name)
            attr.value_widget = \
                    attr.widget_type(self.other_attr_frame, width=10)
            attr.value_widget.insert(0, self.get_attribute(attr.name))
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
        self.app.remove_device(self.device_name)
        self.destroy()

    def _get_attribute(self, attr):
        """Return value of |attribute| via tango device proxy.

        Args:
            attr(str): attribute.

        """
        return self.tango_device.read_attribute(attr).value

    def _set_attribute(self, attr, val):
        """Set value to attribute via tango device proxy.

        Args:
            attr(str): attribute.
            val: value.

        """
        self.tango_device.write_attribute(attr, val)

    def _update_mode(self):
        """Turn on/off expert mode according to |expert_chkbtn|."""
        if self.is_expert.get() == 0:
            self.other_attr_frame.grid_remove()
        else:
            self.other_attr_frame.grid()

    def log(self, out):
        """Log essential information. Called at each step of scanning if
        |is_always_log| is True or it is the device to be scanned.

        Args:
            out (file object): where log is written.

        """
        out.write("%s::%s::DefaultLog\n" % (self.device_type, self.device_name))

    def get_attribute(self, attr):
        """Get attribute value. Should take care of all attributes in
        |common_attr|, |scannable_attr| and |other_attr|.

        Args:
            attr(str): attribute.

        """
        pass

    def set_attribute(self, attr, val):
        """Set attribute value. Should take care of all attributes in
        |common_attr|, |scannable_attr| and |other_attr|. Return False if
        failed.

        Args:
            attr(str): attribute.
            val: value.

        """
        pass


class LimaCCDsDevice(DeviceBase):
    """Device widget of Camera.

    Common attributes:
        - Exposure time: tk.Entry

    Other attributes:
        - Number of frames: tk.Entry

    """
    def __init__(self, app, master, name):
        DeviceBase.__init__(self, app, master, name)

        self.device_type = "LimaCCDs"
        self.device_name = name
        self.is_always_log = True
        self.common_attr = [Attribute("Exposure Time", tk.Entry)]
        self.scannable_attr = self.common_attr
        self.other_attr = [Attribute("Number of frames", tk.Entry),
                           Attribute("Saving next number", tk.Entry)]

        # TODO: this is a workaround of the original attribute
        # "saving_next_number" which has some weird bugs.
        self.saving_next_number = 0

        self._create_widgets()

    def log(self, out):
        """Log essential information. Called at each step of scanning if
        |is_always_log| is True or it is the device to be scanned.

        Args:
            out (file object): where log is written.

        Log:
            captured images stored in |app.log_path|.
            LimaCCDs::DeviceName::Exposure Time = 1.0
            LimaCCDs::DeviceName::ImageFile0 = CS0001.raw

        """
        nb_frames = self.tango_device.acq_nb_frames
        # Prevent acquisition not finished error.
        time.sleep(1.0)
        self.tango_device.prepareAcq()
        self.tango_device.startAcq()
        # Wait for capturing finish.
        while self.tango_device.last_image_ready != nb_frames - 1:
            time.sleep(0.05)
        self.tango_device.saving_directory = os.path.dirname(out.name)
        self.tango_device.saving_prefix = "LIMA"
        self.tango_device.saving_suffix = "raw"
        self.tango_device.saving_format = "RAW"
        self.tango_device.saving_overwrite_policy = "OVERWRITE"
        expo = self._get_attribute("acq_expo_time")
        content = "%s::%s::Exposure Time = %s\n" % \
                (self.device_type, self.device_name, str(expo))
        for image_idx in range(nb_frames):
            image_file_name = "%s%04d%s" % (self.tango_device.saving_prefix,
                                            self.saving_next_number,
                                            self.tango_device.saving_suffix)
            self.tango_device.saving_next_number = self.saving_next_number
            self.tango_device.writeImage(image_idx)
            self.saving_next_number += 1
            content += "%s::%s::ImageFile%d = %s\n" % (self.device_type,
                                                       self.device_name,
                                                       image_idx,
                                                       image_file_name)
        out.write(content)

    def get_attribute(self, attr):
        """Get attribute value. Should take care of all attributes in
        |common_attr|, |scannable_attr| and |other_attr|.

        Args:
            attr(str): attribute.

        """
        if attr == "Exposure Time":
            return self._get_attribute("acq_expo_time")
        elif attr == "Number of frames":
            return self._get_attribute("acq_nb_frames")
        elif attr == "Saving next number":
            return self.saving_next_number
        else:
            print "Error: unknown attribute %s." % attr
            return None

    def set_attribute(self, attr, val):
        """Set attribute value. Should take care of all attributes in
        |common_attr|, |scannable_attr| and |other_attr|. Return False if
        failed.

        Args:
            attr(str): attribute.
            val: value.

        """
        if attr == "Exposure Time":
            min_et, max_et = self._get_attribute("valid_ranges")[:2]
            if val < min_et or val > max_et:
                print "Error: illegal exposure time %s." % val
                return False
            self._set_attribute("acq_expo_time", val)
        elif attr == "Number of frames":
            self._set_attribute("acq_nb_frames", val)
        elif attr == "Saving next number":
            self.saving_next_number = val
        else:
            print "Error: unknown attribute %s." % attr
            return False
        return True


class MotorDevice(DeviceBase):
    """Device widget of Motor.

    Common attributes:
        - Position: tk.Entry

    Other attributes:
        - Step per unit: tk.Entry

    """
    def __init__(self, app, master, name):
        DeviceBase.__init__(self, app, master, name)

        self.device_type = "Motor"
        self.device_name = name
        self.is_always_log = False
        self.common_attr = [Attribute("Position", tk.Entry)]
        self.scannable_attr = self.common_attr
        self.other_attr = [Attribute("Step per unit", tk.Entry)]

        self._create_widgets()

    def log(self, out):
        """Log essential information. Called at each step of scanning if
        |is_always_log| is True or it is the device to be scanned.

        Args:
            out (file object): where log is written.

        Log:
            Motor::DeviceName::Position = 0.0

        """
        pos = self._get_attribute("position")
        content = "%s::%s::Position = %s\n" % \
                (self.device_type, self.device_name, str(pos))
        out.write(content)

    def get_attribute(self, attr):
        """Get attribute value. Should take care of all attributes in
        |common_attr|, |scannable_attr| and |other_attr|.

        Args:
            attr(str): attribute.

        """
        if attr == "Position":
            return self._get_attribute("position")
        elif attr == "Step per unit":
            return self._get_attribute("step_per_unit")
        else:
            print "Error: unknown attribute %s." % attr
            return None

    def set_attribute(self, attr, val):
        """Set attribute value. Should take care of all attributes in
        |common_attr|, |scannable_attr| and |other_attr|. Return False if
        failed.

        Args:
            attr(str): attribute.
            val: value.

        """
        if attr == "Position":
            # Must use device alias.
            device_alias = self.app.tango.get_device_alias(self.device_name)
            self.app.tango.run_macro(["mv", device_alias, str(val)])
        elif attr == "Step per unit":
            self._set_attribute("step_per_unit", val)
        else:
            print "Error: unknown attribute %s." % attr
            return False
        return True


class ScanEntry(tk.Frame):
    """Scan widget for a single attribute.

    Args:
        master: reference to parent widget.
        device (str): device to be scanned.
        attr (str): attribute to be scanned.

    Attributes:
        device (str): device to be scanned.
        attr (str): attribute to be scanned.

    """
    def __init__(self, master, device, attr):
        tk.Frame.__init__(self, master, borderwidth=2, relief=tk.RAISED)

        self.device = device
        self.attr = attr

        self._create_widgets()

    def _create_widgets(self):
        """Create and configure all widgets."""
        # Accessibility.
        self.enabled = tk.IntVar(self, 1)
        self.state_chkbtn = tk.Checkbutton(self, variable=self.enabled,
                                           command=self.update_state)
        # Device and attributes.
        self.device_attr_label = tk.Label(self,
                                          text=self.device + "::" + self.attr)
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
                                    command=self.destroy)

        self.columnconfigure(1, weight=1)
        self.state_chkbtn.grid(row=0, column=0)
        self.device_attr_label.grid(row=0, column=1, sticky=(W))
        self.start_entry.grid(row=0, column=2)
        self.end_entry.grid(row=0, column=3)
        self.step_entry.grid(row=0, column=4)
        self.delete_btn.grid(row=0, column=5)

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

    def update_state(self):
        """Enable or disable widgets according to |state_chkbtn|."""
        if self.enabled.get() == 0:
            gui.Application.change_state(self, False)
            gui.Application.change_state(self.state_chkbtn, True)
            gui.Application.change_state(self.delete_btn, True)
        else:
            gui.Application.change_state(self, True)


if __name__ == "__main__":
    ROOT = tk.Tk()
    ATTR = Attribute("TEST_ATTR")

    LIMACCD = LimaCCDsDevice(ROOT, ROOT, "TEST_CAMERA")
    MOTOR = MotorDevice(ROOT, ROOT, "TEST_CAMERA")
    ENTRY = ScanEntry(ROOT, "TEST_DEVICE", "TEST_ATTR")
    ROOT.destroy()

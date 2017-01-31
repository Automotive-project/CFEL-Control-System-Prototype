#!/usr/bin/env python
# pylint: disable=attribute-defined-outside-init, fixme, line-too-long, no-self-use, too-few-public-methods, too-many-ancestors, too-many-instance-attributes, too-many-public-methods, unused-variable
"""This module contains custom widgets for Control System GUI.

Tkinter is used for GUI.

"""

import Tkinter as tk
from Tkinter import N, S, E, W

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
        common_attr (list of |Attribute|): common attributes.
        other_attr (list of |Attribute|):
                other attributes which are displayed only in expert mode.

    """
    def __init__(self, app, master, name):
        tk.Frame.__init__(self, master, name=name.lower(), borderwidth=2,
                          relief=tk.RAISED)

        self.app = app
        self.device_type = "DeviceBase"
        self.device_name = "DeviceBase"
        self.common_attr = []
        # FIX: Is |common_attr| == scannable_attr?
        self.scannable_attr = self.common_attr
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
        self.app.remove_device(self.device_name)
        self.destroy()

    def _update_mode(self):
        """Turn on/off expert mode according to |expert_chkbtn|."""
        if self.is_expert.get() == 0:
            self.other_attr_frame.grid_remove()
        else:
            self.other_attr_frame.grid()

    def log(self, out):
        """Log essential information. Called at each step during scanning."""
        out.write("This is default log from device %s.\n" % self.device_name)

    def set_attr(self, attr, value):
        """Set attribute value. Should take care of all attributes in
        |scannable_attr|.

        """
        pass


class LimaCCDsDevice(DeviceBase):
    """Device widget of Camera.

    Common attributes:
        - Exposure time: tk.Entry

    Other attributes:
        - Aperture: tk.Entry

    ['acq_status', 'saving_next_number', 'debug_modules', 'camera_pixelsize', 'acq_mode', 'user_detector_name', 'video_roi', 'video_active', 'acc_mode', 'video_bin', 'config_available_module', 'image_height', 'concat_nb_frames', 'acc_dead_time', 'acc_offset_before', 'shared_memory_names', 'acq_expo_time', 'last_base_image_ready', 'ready_for_next_acq', 'saving_managed_mode', 'acc_live_time', 'video_last_image', 'last_counter_ready', 'acc_saturated_active', 'video_gain', 'image_type', 'last_image', 'shutter_mode', 'image_width', 'image_sizes', 'acc_time_mode', 'debug_types', 'plugin_list', 'camera_type', 'instrument_name', 'latency_time', 'acq_trigger_mode', 'acc_max_expo_time', 'image_events_push_data', 'image_events_max_rate', 'shutter_manual_state', 'debug_modules_possible', 'saving_index_format', 'acc_nb_frames', 'saving_header_delimiter', 'image_flip', 'saving_common_header', 'debug_types_possible', 'acc_saturated_cblevel', 'ready_for_next_image', 'image_rotation', 'acc_expo_time', 'acc_saturated_threshold', 'video_exposure', 'acc_threshold_before', 'image_bin', 'saving_suffix', 'saving_prefix', 'lima_type', 'acq_nb_frames', 'acq_status_fault_error', 'shared_memory_active', 'video_live', 'config_available_name', 'last_image_ready', 'saving_format', 'write_statistic', 'buffer_max_memory', 'image_roi', 'video_mode', 'video_last_image_counter', 'last_image_acquired', 'saving_frame_per_file', 'shutter_close_time', 'camera_model', 'saving_directory', 'saving_mode', 'video_source', 'last_image_saved', 'saving_overwrite_policy', 'plugin_type_list', 'valid_ranges', 'shutter_open_time', 'State', 'Status']

    """
    def __init__(self, app, master, name):
        DeviceBase.__init__(self, app, master, name)

        self.device_type = "LimaCCDs"
        self.device_name = name
        self.common_attr = [Attribute("Exposure Time", tk.Entry)]
        self.other_attr = [Attribute("Aperture", tk.Entry)]

        self._create_widgets()

    def log(self, out):
        """Capture and store image. Log image path and attributes in |out|."""
        pass

    def set_attr(self, attr, value):
        """Set attribute value. Should take care of all attributes in
        |scannable_attr|.

        """
        pass


class MotorDevice(DeviceBase):
    """Device widget of Camera.

    Common attributes:
        - Exposure time: tk.Entry

    Other attributes:
        - Aperture: tk.Entry

    ['Instrument', 'SimulationMode', 'Acceleration', 'Step_per_unit', 'Velocity', 'Base_rate', 'Sign', 'Limit_switches', 'DialPosition', 'Deceleration', 'Offset', 'Position', 'Backlash', 'LowerLimitSwitch', 'UpperLimitSwitch', 'Power', 'State', 'Status']

    """
    def __init__(self, app, master, name):
        DeviceBase.__init__(self, app, master, name)

        self.device_type = "Camera"
        self.device_name = name
        self.common_attr = [Attribute("Position", tk.Entry), Attribute("Speed", tk.Entry)]
        self.other_attr = [Attribute("Step size", tk.Entry)]

        self._create_widgets()

    def log(self, out):
        """Log attributes in |out|."""
        pass

    def set_attr(self, attr, value):
        """Set attribute value. Should take care of all attributes in
        |scannable_attr|.

        """
        if attr == "Position":
            device_alias = self.app.tango.get_device_alias(self.device_name)
            self.app.tango.door.runmacro(["mv", device_alias, str(value)])
        else:
            print "Error: unknown scannable attribute %s." % attr


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

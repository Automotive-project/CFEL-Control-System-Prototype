#!/usr/bin/env python

import Tkinter as tk
from Tkinter import N, S, E, W

class Attribute:
    def __init__(self, name="ATTR_NAME", w_type=tk.Widget, w=tk.Widget()):
        self.name = name
        self.widget_type = w_type
        self.name_widget = w
        self.value_widget = w


class DeviceBase(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, borderwidth=2, relief=tk.RAISED)

        self.device_type = "DEVICE_TYPE"
        self.device_name = "DEVICE_NAME"
        self.common_attr = [Attribute("COMMON_ATTR", tk.Entry)]
        self.other_attr = [Attribute("OTHER_ATTR", tk.Entry)]

    def toggle_expert(self):
        if self.is_expert.get() == 0:
            for attr in self.other_attr:
                attr.name_widget.grid_remove()
                attr.value_widget.grid_remove()
        else:
            for attr in self.other_attr:
                attr.name_widget.grid()
                attr.value_widget.grid()

    def create_widgets(self):
        self.device_label = tk.Label(self, text=self.device_name)
        # Accessibility.
        self.is_expert = tk.IntVar(self)
        self.is_expert.set(0)
        self.expert_chkbtn = tk.Checkbutton(self, variable=self.is_expert, command=self.toggle_expert)
        for attr in self.common_attr:
            attr.name_widget = tk.Label(self, text=attr.name)
            attr.value_widget = attr.widget_type(self)
        for attr in self.other_attr:
            attr.name_widget = tk.Label(self, text=attr.name)
            attr.value_widget = attr.widget_type(self)

        self.device_label.grid(row=0, column=0, sticky=(E, W), padx=(5,0))
        self.expert_btn.grid(row=0, column=1, sticky=(E, W), padx=(0,5))
        for idx, attr in enumerate(self.common_attr):
            attr.name_widget.grid(row=idx+1, column=0, sticky=(E, W), padx=(5,0))
            attr.value_widget.grid(row=idx+1, column=1, sticky=(E, W), padx=(0,5))
        for idx, attr in enumerate(self.other_attr):
            attr.name_widget.grid(row=len(self.common_attr)+idx+1, column=0, sticky=(E, W), padx=(5,0)).grid_remove()
            attr.value_widget.grid(row=len(self.common_attr)+idx+1, column=1, sticky=(E, W), padx=(0,5)).grid_remove()

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)


"""Naming convention: TypeDevice"""
class CameraDevice(DeviceBase):
    def __init__(self, master, name):
        DeviceBase.__init__(self, master)

        self.device_type = "Camera"
        self.device_name = name
        self.common_attr = [("Exposure Time", tk.Entry)]
        self.other_attr = [("Aperture", tk.Entry)]

        self.create_widgets()


class ScanEntry(tk.Frame):
    def __init__(self, master, device, attr):
        tk.Frame.__init__(self, master, borderwidth=2, relief=tk.RAISED)

        # Accessibility.
        self.enabled = tk.IntVar(self)
        self.enabled.set(1)
        self.state_chkbtn = tk.Checkbutton(self, variable=self.enabled, command=self.toggle_state)
        # Device and attributes.
        self.device_attr_label = tk.Label(self, text=device + "::" + attr)
        # Start, end, step.
        entry_width = 5
        self.start_entry = tk.Entry(self, fg="grey", width=entry_width)
        self.start_entry.insert(0, "start")
        self.start_entry.bind("<FocusIn>", self.on_entry_focusin)
        self.start_entry.bind("<FocusOut>", self.on_entry_focusout)
        self.end_entry = tk.Entry(self, fg="grey", width=entry_width)
        self.end_entry.insert(0, "end")
        self.end_entry.bind("<FocusIn>", self.on_entry_focusin)
        self.end_entry.bind("<FocusOut>", self.on_entry_focusout)
        self.step_entry = tk.Entry(self, fg="grey", width=entry_width)
        self.step_entry.insert(0, "step")
        self.step_entry.bind("<FocusIn>", self.on_entry_focusin)
        self.step_entry.bind("<FocusOut>", self.on_entry_focusout)
        # Delete.
        self.delete_btn = tk.Button(self, text="X", fg="white", bg="red", width=1, command=self.delete)

        self.columnconfigure(1, weight=1)
        self.availability_chkbtn.grid(row=0, column=0)
        self.device_attr_label.grid(row=0, column=1, sticky=(W))
        self.start_entry.grid(row=0, column=2)
        self.end_entry.grid(row=0, column=3)
        self.step_entry.grid(row=0, column=4)
        self.delete_btn.grid(row=0, column=5)

    def toggle_state(self):
        if self.enabled.get() == 0:
            self.device_label.config(fg="grey")
            self.attr_label.config(fg="grey")
            self.start_entry.config(state=tk.DISABLED)
            self.end_entry.config(state=tk.DISABLED)
            self.step_entry.config(state=tk.DISABLED)
        else:
            self.device_label.config(fg="black")
            self.attr_label.config(fg="black")
            self.start_entry.config(state=tk.NORMAL)
            self.end_entry.config(state=tk.NORMAL)
            self.step_entry.config(state=tk.NORMAL)

    def on_entry_focusin(self, event):
        if event.widget.get() in ["start", "end", "step"]:
            event.widget.delete(0, "end")
            event.widget.config(fg="black")

    def on_entry_focusout(self, event):
        if event.widget.get():
            return
        event.widget.config(fg="grey")
        if event.widget == self.start_entry:
            event.widget.insert(0, "start")
        elif event.widget == self.end_entry:
            event.widget.insert(0, "end")
        elif event.widget == self.step_entry:
            event.widget.insert(0, "step")

    def delete(self):
        self.destroy()
        # TODO: delete from |self.scan_entries|?


if __name__ == "__main__":
    root = tk.Tk()
    entry = ScanEntry(root, "DEVICE", "ATTR")
    root.destroy()

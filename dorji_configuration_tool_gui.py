#!/usr/bin/python3
# AhmetAlperenBULUT
# https://github.com/ahmetalperenbulut/dorji_drf_tool

import tkinter
import tkinter.ttk
import dorji_configuration_tool
from serial.tools import list_ports
import serial
import sys


class DorjiConfigurationGUI:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.title("Dorji RF Module Configuration Tool")
        self.tk.geometry('600x500')
        self.tk.resizable(width=False, height=False)
        self.tk.grid_columnconfigure(0, weight=1)
        self.tk.grid_rowconfigure(0, weight=1)
        self.tk.configure(background="#c0c0c0")
        self.communication = dorji_configuration_tool.dorji_rf_module()
        # Main Frame
        content = tkinter.Frame(self.tk, height=500, width=600)
        content.grid(row=0, column=0, sticky=tkinter.N)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        content.grid_rowconfigure(2, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_propagate(0)
        # Sub Frames
        configuration_frame = tkinter.Frame(
            content, highlightthickness=1, highlightbackground="black", height=250, width=500)
        configuration_frame.grid(row=0, column=0, pady=(50, 0))
        configuration_frame.grid_rowconfigure(0, weight=1)
        configuration_frame.grid_rowconfigure(1, weight=1)
        configuration_frame.grid_columnconfigure(0, weight=1)
        configuration_frame.grid_propagate(0)

        serial_frame = tkinter.Frame(content, height=100, width=500)
        serial_frame.grid(row=1, column=0, sticky=tkinter.N, pady=(30, 0))
        # serial_frame.grid_rowconfigure(0, weight=1)
        serial_frame.grid_columnconfigure(0, weight=1)
        serial_frame.grid_propagate(0)

        outputs_frame = tkinter.Frame(
            content, highlightthickness=1, highlightbackground="#F0f0f0", bg="#c0c0c0", width=600, height=30)
        outputs_frame.grid(row=2, column=0, sticky=tkinter.S)
        outputs_frame.grid_rowconfigure(0, weight=1)
        outputs_frame.grid_columnconfigure(0, weight=1)
        outputs_frame.grid_propagate(0)

        rfframe = tkinter.LabelFrame(
            configuration_frame, text="RF Parameters", borderwidth=4, height=125, width=450)
        rfframe.grid(row=0, column=0)
        rfframe.grid_propagate(0)

        # ROW 1
        # Freq columns
        freq_lbl1 = tkinter.Label(rfframe, text="RF Frequency:")
        freq_lbl1.grid(row=0, column=0, padx=(
            15, 0), pady=(0, 15), sticky=tkinter.W)
        self.freq_txt = tkinter.Entry(rfframe, width=7)
        self.freq_txt.grid(row=0, column=1, padx=(5, 0),
                           pady=15, sticky=tkinter.W)
        freq_lbl2 = tkinter.Label(rfframe, text="MHz")
        freq_lbl2.grid(row=0, column=2, padx=(
            2, 0),  pady=15, sticky=tkinter.W)
        # Power columns
        power_lbl = tkinter.Label(rfframe, text="RF Power:")
        power_lbl.grid(row=0, column=3, padx=(
            15, 0), pady=15,  sticky=tkinter.E)
        self.power_combo = tkinter.ttk.Combobox(rfframe, width=7)
        self.power_combo['values'] = ("0 (Min)", 1, 2, 3, 4, 5, 6, "7 (Max)")
        self.power_combo.current(7)  # set the selected item
        self.power_combo.grid(row=0, column=4, padx=(
            7, 0),  pady=15, sticky=tkinter.W)

        # ROW 2
        # TRx Rate columns
        trx_rate_lbl = tkinter.Label(rfframe, text="RF TRx rate:")
        trx_rate_lbl.grid(row=1, column=0, sticky=tkinter.W,
                          padx=(15, 0))
        self.trx_rate_combo = tkinter.ttk.Combobox(rfframe, width=9)
        self.trx_rate_combo['values'] = (
            "1K/1.2K", "2K/2.4K", "5K/4.8K", "10K/9.6K", "20K/19.2K", "40K/38.4K")
        self.trx_rate_combo.current(3)  # set the selected item
        self.trx_rate_combo.grid(row=1, column=1, columnspan=2, padx=(
            5, 0),   sticky=tkinter.W)
        # Wakeup time colums
        wakeup_lbl = tkinter.Label(rfframe, text="Wakeup Time:")
        wakeup_lbl.grid(row=1, column=3,  padx=(15, 0),
                        sticky=tkinter.W)
        self.wakeup_combo = tkinter.ttk.Combobox(rfframe, width=7)
        self.wakeup_combo['values'] = ("50ms", "100ms", "200ms", "400ms",
                                       "600ms", "1.0s", "1.5s", "2.0s", "2.5s", "3.0s", "4.0s", "5.0s")
        self.wakeup_combo.current(5)  # set the selected item
        self.wakeup_combo.grid(row=1, column=4, padx=(
            7, 0), sticky=tkinter.W)

        seriesframe = tkinter.LabelFrame(
            configuration_frame, text="Series Parameters", height=80, width=450, borderwidth=4)
        seriesframe.grid(row=1, column=0)
        seriesframe.grid_propagate(0)
        # ROW 1
        # Series Rate columns
        series_rate_lbl = tkinter.Label(seriesframe, text="Series rate:")
        series_rate_lbl.grid(row=0, column=0, padx=(
            20, 0), pady=(15, 0), sticky=tkinter.W)
        self.series_rate_combo = tkinter.ttk.Combobox(seriesframe, width=9)
        self.series_rate_combo['values'] = (
            "1200bps", "2400bps", "4800bps", "9600bps", "19200bps", "38400bps", "57600bps", "115200bps")
        self.series_rate_combo.current(3)  # set the selected item
        self.series_rate_combo.grid(row=0, column=1, padx=(
            15, 0), pady=(15, 0), sticky=tkinter.W)
        # Series Parity
        series_parity_lbl = tkinter.Label(seriesframe, text="Series parity:")
        series_parity_lbl.grid(row=0, column=2, padx=(
            40, 0), pady=(15, 0), sticky=tkinter.W)
        self.series_parity_combo = tkinter.ttk.Combobox(seriesframe, width=10)
        self.series_parity_combo['values'] = (
            "Disable", "Even parity", "Odd parity")
        self.series_parity_combo.current(0)  # set the selected item
        self.series_parity_combo.grid(row=0, column=3, padx=(
            5, 0), pady=(15, 0), sticky=tkinter.W)

        # Serial Frame

        pcserialframe = tkinter.LabelFrame(
            serial_frame, text="PC Serial", height=80, width=500, borderwidth=4)
        pcserialframe.grid(row=2, column=0)
        pcserialframe.grid_propagate(0)
        pcseries_lbl = tkinter.Label(pcserialframe, text="PC Series:")
        pcseries_lbl.grid(row=0, column=0, sticky=tkinter.W, padx=(
            15, 0), pady=(10, 0))
        self.pcseries_combo = tkinter.ttk.Combobox(pcserialframe, width=12)
        self.pcseries_combo.bind("<Button>", self.pc_series_cb)
        self.pcseries_combo['values'] = self.read_comports()
        if len(self.pcseries_combo['values']) > 0:
            self.pcseries_combo.current(0)  # set the selected item

        self.pcseries_combo.grid(row=0, column=1, padx=(
            20, 0), sticky=tkinter.W, pady=(10, 0))
        
        # Buttons
        write_button = tkinter.Button(
            pcserialframe, text="Write", command=self.write_button_clicked)
        write_button.grid(row=0, column=3, sticky=tkinter.W,
                          padx=(70, 40), pady=(10, 0))
        read_button = tkinter.Button(
            pcserialframe, text="Read", command=self.read_button_clicked)
        read_button.grid(row=0, column=4, sticky=tkinter.W, pady=(10, 0))

        # Outputs frame
        self.outputs_lbl = tkinter.Label(outputs_frame,  bg="#c0c0c0")
        self.outputs_lbl.grid(row=0, column=0, sticky=tkinter.S+tkinter.W)
        self.tk.mainloop()

    def pc_series_cb(self, eventObject):
        
        self.pcseries_combo['values'] = self.read_comports()
        if len(self.pcseries_combo['values']) > 0:
            self.pcseries_combo.current(0)  # set the selected item


    def read_button_clicked(self):
        if self.pcseries_combo.current() < 0:
            return
        

        self.communication.connect(self.pcseries_combo.get(), self.communication._mapping_readable_form(
            self.series_rate_combo.current(), dorji_configuration_tool.Configuration_Values.BAUD_RATE), self.mapping_parity(self.series_parity_combo.current()))
        if self.communication.read_configurations():
            self.freq_txt.delete(0,tkinter.END)
            self.freq_txt.insert(0,self.communication._freq_readable/1000)
            self.power_combo.current(int.from_bytes(self.communication._rf_power,sys.byteorder))
            self.trx_rate_combo.current(int.from_bytes(self.communication._rf_trx_rate,sys.byteorder))
            self.wakeup_combo.current(int.from_bytes(self.communication._wakeup_time,sys.byteorder))
        self.communication.disconnect()

    def write_button_clicked(self):
        if self.write_form_elements_to_communication():
            self.communication.connect(self.pcseries_combo.get(), self.communication._mapping_readable_form(
            self.series_rate_combo.current(), dorji_configuration_tool.Configuration_Values.BAUD_RATE), self.mapping_parity(self.series_parity_combo.current()))
            self.communication._write_configurations()
            self.communication.disconnect()

    def write_form_elements_to_communication(self):
        try:
            if self.freq_txt.get().isdigit():
                self.communication._freq = (int(self.freq_txt.get())*1000).to_bytes(3,'big')
            else:
                self.communication._freq = (int(float(self.freq_txt.get()))*1000).to_bytes(3,'big')
            self.communication._rf_trx_rate = self.trx_rate_combo.current().to_bytes(1, 'big')
            self.communication._baud_rate = self.series_rate_combo.current().to_bytes(1, 'big')
            self.communication._rf_power = self.power_combo.current().to_bytes(1, 'big')
            self.communication._parity = self.series_parity_combo.current().to_bytes(1, 'big')
            self.communication._wakeup_time = self.wakeup_combo.current().to_bytes(1, 'big')
            

            return True
        except Exception as e:
            print(e)
            return False


    def read_comports(self):
        comports = tuple()
        for port in list_ports.comports():
            comports += (port.device,)
        print(comports)
        return comports

    def mapping_parity(self, val):
        if val == 0:
            return serial.PARITY_NONE
        elif val == 1:
            return serial.PARITY_EVEN
        elif val == 2:
            return serial.PARITY_ODD


a = DorjiConfigurationGUI()

import tkinter as tk
from tkinter import ttk
from calculations import Calculations


g_area=float()
hx_sel= int()

#class containing the first frame in the program
class Introframe(ttk.Frame):
    def __init__(self, container,parent):
        super().__init__(container)

        self["style"] = "Background.TFrame"
        greetings = ttk.Label(self, text="Geothermal Plant Design Program",
                              font="Helvetica 15", style="LabelText.TLabel")
        greetings.grid(row=0, column=0, padx=20, pady=20, sticky="W")

        selection_frame = ttk.Frame(self, style="Window.TFrame")
        selection_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

        selection_label = ttk.Label(selection_frame, style="LightText.TLabel", text="Select the type of heat exchanger")
        selection_label.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.storage_var = tk.StringVar()
        horizontal = ttk.Radiobutton(selection_frame, text="Horizontal Heat Exchanger", style="Radio.TRadiobutton",
                                     value="Horizontal", variable=self.storage_var, cursor='hand2',
                                     command=self.selecting_hx)
        vertical = ttk.Radiobutton(selection_frame, text="Vertical Heat Exchanger", style="Radio.TRadiobutton",
                                   value="Vertical", variable=self.storage_var,
                                   command=self.selecting_hx)
        horizontal.grid(row=2, column=0, padx=20, pady=10, sticky="W")
        vertical.grid(row=3, column=0, padx=20, pady=10, sticky="W")

        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

        next_button = ttk.Button(button_container,
                                 text="Next",
                                 cursor="hand2",
                                 style="ButtonColour.TButton",
                                 command=lambda: parent.show_frames(EnergyDemand))
        next_button.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    def selecting_hx(self):
        if self.storage_var.get() == "Horizontal":
            global hx_sel
            hx_sel = 0
        elif self.storage_var.get() == "Vertical":
            hx_sel = 1


#class that contains the second frame
class EnergyDemand(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)

        self["style"] = "Background.TFrame"
        title_frame = ttk.Frame(self, style= "Background.TFrame")
        title_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        title_label = ttk.Label(title_frame,
                                text="Energy Demand", style="LabelText.TLabel")
        title_label.grid(row=0, column=0, pady=10, sticky="W")

        area_frame = ttk.Frame(self, style="Background.TFrame")
        area_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

        self.building_area = tk.StringVar()
        self.Q_d = tk.StringVar()  #Qd - heat supplied in a day [KWh]

        area_label = ttk.Label(area_frame,
                               text="Enter the area of the building in m^2",
                               style="LightText.TLabel")
        area_label.grid(row=0, column=0, sticky="W")
        area_input = ttk.Entry(area_frame,
                               textvariable=self.building_area,
                               style="EntryStyle.TEntry", width=15)
        area_input.grid(row=0, column=1, sticky="W")
        area_input.focus()
        area_input.bind("<Any-KeyPress>", self.activate_calculate)

        #calculate line
        calculate_label=ttk.Label(area_frame,
                                  text="Click calculate button for Energy Demand",
                                  style="LightText.TLabel")
        calculate_label.grid(row=1, column=0, sticky="EW")

        self.calculate_button=ttk.Button(area_frame,
                                         text="Calculate",
                                         style= "ButtonColour.TButton",
                                         command=lambda:self.call_calculations(self.building_area),
                                         state='disabled')
        self.calculate_button.grid(row=1, column=1, sticky="EW")
        self.calculate_button.bind('<Return>', lambda e: self.call_calculations(self.building_area))

        #variables

        self.HC_area = tk.StringVar(value=0.045)
        #"HC_area - German standard heat consumption per unit area [KW/m^2]"
        self.P_hg = tk.StringVar()              #"P_hg - heat output generated"
        self.P_hw = tk.StringVar()
        self.P_hwp = tk.StringVar(value=0.3)
        self.N = tk.StringVar()
        # "P_hw - heat output for hot water generation [KW]"
        # "P_hwp - heat output for hot water per person , 0.25 kw/person to 0.35 kw/ person"
        # "N - no of people"

        #Heat demand
        heat_day_label = ttk.Label(area_frame,
                                   text="Heat Output : ",
                                   style="LightText.TLabel")
        heat_day_label.grid(row=2, column=0, sticky="EW")
        heat_day_output = ttk.Label(area_frame, textvariable=self.Q_d,
                                    justify="right",
                                    style="LightText.TLabel")
        heat_day_output.grid(row=2, column=1, sticky="EW")
        unit_label = ttk.Label(area_frame, text="KW",
                               style="LightText.TLabel")
        unit_label.grid(row=2, column=2, sticky="W")

        for child in area_frame.winfo_children():
            child.grid_configure(padx=10, pady=10)

        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

        back_button = ttk.Button(button_container,
                                 text="Back",
                                 cursor="hand2",
                                 style="ButtonColour.TButton",
                                 command=lambda: parent.show_frames(Introframe))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        next_button = ttk.Button(button_container,
                                 text="Next",
                                 cursor="hand2",
                                 style="ButtonColour.TButton",
                                 command=lambda: parent.change_frame_name(3))
        next_button.grid(row=0, column=1, padx=10, pady=10, sticky="E")

    def activate_calculate(self,arg):
        try:
            if float(self.building_area.get()) >=1 and float(self.building_area.get()) <=1000 :
                self.calculate_button.config(state="active")
        except ValueError:
            pass

    def call_calculations(self,area):
        try:
            float_area = float(area.get())
            self.calc = Calculations()
            self.Q_d.set(self.calc.demand_calculator(float_area))
            global g_area
            g_area = float_area

        except ValueError:
            pass


#function for retrieving the area entered by the user
def get_g_area():
    global g_area

    return g_area


#function for retrieving the type of heat exchanger chosen by the user
def get_hx_selection():
    global hx_sel

    return hx_sel

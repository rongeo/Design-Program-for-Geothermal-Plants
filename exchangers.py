import tkinter as tk
from tkinter import ttk
from calculations import Calculations
from baseframe import get_hx_selection
import pandas as pd
import webbrowser


#class that displays the pump characteristics
class PumpSelection(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)

        self["style"] = "Background.TFrame"
        area_frame = ttk.Frame(self, style= "Background.TFrame")
        area_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        self.main=parent
        #variables
        self.cop=tk.StringVar()
        self.electric_power=tk.StringVar()
        self.heat_power=tk.StringVar()
        self.name_pump=tk.StringVar()

        #Heading
        greetings = ttk.Label(area_frame,
                              text="Selected Pump Characteristics",
                              style = "LabelText.TLabel")
        greetings.grid(row=0, column=0,pady=10, sticky="W")
        name_label = ttk.Label(area_frame, text="Name of the Pump",
                               style= "LightText.TLabel")
        name_label.grid(row=1, column=0, sticky="W")
        name_output = ttk.Label(area_frame, textvariable=self.name_pump,
                                style= "LightText.TLabel")
        name_output.grid(row=1, column=1, sticky="W")

        heat_label = ttk.Label(area_frame, text="Heat Output of Pump",
                               style= "LightText.TLabel")
        heat_label.grid(row=2, column=0, sticky="W")
        heat_output = ttk.Label(area_frame, textvariable=self.heat_power,
                                style= "LightText.TLabel")
        heat_output.grid(row=2, column=1, sticky="W")

        electric_label=ttk.Label(area_frame, text="Electric Output of Pump",
                                 style= "LightText.TLabel")
        electric_label.grid(row=3, column=0, sticky="W")
        electric_output = ttk.Label(area_frame, textvariable=self.electric_power,
                                    style= "LightText.TLabel")
        electric_output.grid(row=3, column=1, sticky="W")

        COP_label = ttk.Label(area_frame, text="COP",
                              style= "LightText.TLabel")
        COP_label.grid(row=4, column=0, sticky="W")
        COP_output = ttk.Label(area_frame, textvariable=self.cop,
                               style= "LightText.TLabel")
        COP_output.grid(row=4, column=1, sticky="W")

        calculate_button = ttk.Button(area_frame,
                                      text="Display Heat Pump",
                                      command=lambda: self.print_pump_chara(),
                                      style= "ButtonColour.TButton")
        calculate_button.grid(row=5, column=1, sticky="EW")
        calculate_button.focus()
        calculate_button.bind('<Return>', lambda event:self.print_pump_chara())

        button_container = ttk.Frame(self,style= "Background.TFrame")
        button_container.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

        back_button = ttk.Button(button_container,
                                 text="Back",
                                 cursor="hand2",
                                 command=lambda: parent.change_frame_name(2),
                                 style= "ButtonColour.TButton")
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        next_button = ttk.Button(button_container,
                                 text="Next",
                                 cursor="hand2",
                                 command=lambda: parent.change_frame_name(self.hx_decider()),
                                 style= "ButtonColour.TButton")
        next_button.grid(row=0, column=1, padx=10, pady=10, sticky="E")

        for child in area_frame.winfo_children():
            child.grid_configure(padx=10, pady=10)

    #function that decides the next frame
    def hx_decider(self):
        hx_value= get_hx_selection()

        if hx_value ==0:
            return 4
        elif hx_value ==1:
            return 5

    #function that prints the selected pump characteristics
    def print_pump_chara(self):
        self.cal=Calculations()
        area=self.main.pass_on_area()

        p_h=self.cal.demand_calculator(area)

        self.cal.heatpump_selector(p_h)
        self.electric_power.set(value=self.cal.P_e_cons)
        self.heat_power.set(value=self.cal.P_h_p)
        self.name_pump.set(value=self.cal.name)
        self.cop.set(value=self.cal.COP_hp)


#class that contains the frame of horizontal heat exchanger
class HorizontalHE(ttk.Frame):
    def __init__(self,container,parent,*args,**kwargs):
        super().__init__(container)

        self["style"] = "Background.TFrame"
        name_frame=ttk.Frame(self,style= "Background.TFrame")
        name_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        area_frame = ttk.Frame(self,style= "Background.TFrame")
        area_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

        self.main = parent
        self.soil_type = tk.StringVar()
        self.area_hx=tk.StringVar()
        self.dbnloops=tk.StringVar()
        self.list_ok=bool()
        self.radio_ok=bool()

        greetings = ttk.Label(name_frame,
                              text="Horizontal Ground Heat Exchanger",
                              style= "LabelText.TLabel")
        greetings.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        selection_label = ttk.Label(area_frame, text="Select the Type of Soil",
                                    style= "LightText.TLabel")
        selection_label.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        #reading the abstraction coefficients from csv file
        ac = pd.read_csv('abstraction_coeff.csv',header=0)
        AC_dict = ac.to_dict(orient='records')

        soil = tuple()
        for i in range(len(AC_dict)):
            soil += (AC_dict[i]['Soil Type'],)

        selected_type = tk.StringVar(value=soil)

        #Displaying the soil type for selection
        self.types_box = tk.Listbox(area_frame, listvariable=selected_type,
                                    height=4, width=30,
                                    selectmode='browse')
        self.types_box.grid(row=2, column=0, sticky="EW")

        scrollbar = ttk.Scrollbar(area_frame,orient='vertical',
                                  command=self.types_box.yview)
        self.types_box['yscrollcommand'] = scrollbar.set

        scrollbar.grid(column=1,row=2,sticky='ns')

        self.types_box.bind('<<ListboxSelect>>', lambda e: self.button_activator(1))

        #providing link for finding the type of soil
        link_label=ttk.Label(area_frame, text="Click here for soil information at a location",
                             cursor='hand2',
                             style= "LightText.TLabel")
        link_label.grid(row=3, column=0, sticky="EW")
        link_label.bind("<Button-1>", lambda e: self.surf_web())

        selection_label = ttk.Label(area_frame, text="Specify the usage in hours per year",
                                    style= "LightText.TLabel")
        selection_label.grid(row=1, column=2, sticky="EW")

        #Selection of the annual usage with the help of buttons
        self.annual_cons = tk.StringVar()
        annual_1800 = ttk.Radiobutton(area_frame, text="Annual usage of 1800 hours",
                                      value=1800, variable=self.annual_cons,
                                      style= "Radio.TRadiobutton",
                                      command=lambda:self.button_activator(2))
        annual_2400 = ttk.Radiobutton(area_frame, text="Annual usage of 2400 hours",
                                      value=2400, variable=self.annual_cons,
                                      style= "Radio.TRadiobutton",
                                      command=lambda:self.button_activator(2))
        annual_1800.grid(row=2, column=2, sticky="E")
        annual_2400.grid(row=3, column=2, sticky="E")

        #button for calculating the results
        self.save_button = ttk.Button(area_frame,
                                      text="Calculate",
                                      command=lambda: self.activate_selections(),
                                      style= "ButtonColour.TButton",
                                      state="disabled")
        self.save_button.grid(row=4, column=2,pady=10, sticky="EW")

        #displaying the obtained results
        second_frame = ttk.Frame(self,style="Background.TFrame")
        second_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")
        area_label = ttk.Label(second_frame, text="Area required for Heat Exchanger: ",
                               style="LightText.TLabel")
        area_label.grid(row=0, column=0, sticky="W")
        area_output = ttk.Label(second_frame, textvariable=self.area_hx,
                                 style="LightText.TLabel")
        area_output.grid(row=0, column=1, sticky="W")
        area_unit = ttk.Label(second_frame, text="m^2",
                              style="LightText.TLabel")
        area_unit.grid(row=0, column=2, sticky="W")

        distance_label = ttk.Label(second_frame, text="Distance between the loops: ",
                                   style="LightText.TLabel")
        distance_label.grid(row=1, column=0, sticky="W")
        distance_output = ttk.Label(second_frame, textvariable=self.dbnloops,
                                    style="LightText.TLabel")
        distance_output.grid(row=1, column=1, sticky="W")
        distance_unit = ttk.Label(second_frame, text="m",
                                  style="LightText.TLabel")
        distance_unit.grid(row=1, column=2, sticky="W")

        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")

        for child in second_frame.winfo_children():
            child.grid_configure(padx=10, pady=10)

        back_button = ttk.Button(button_container,
                                 text="Back",
                                 cursor="hand2",
                                 command=lambda: parent.change_frame_name(3),
                                 style="ButtonColour.TButton")
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    #function for surfing the web
    def surf_web(self):
        webbrowser.open_new('https://www.thermomap.eu/')

    #function for checking the required values are entered before calculation
    def button_activator(self,val,*args):
        try:
            if val==1:
                self.list_ok=True
            elif val==2:
                self.radio_ok=True

            if self.list_ok and self.radio_ok:
                self.save_button.config(state="active")
        except UnboundLocalError:
            pass

    #function for passing values to the calculation section of program
    def activate_selections(self):
        k= self.types_box.curselection()
        self.soil_type.set(k[0])

        self.cal = Calculations()
        area = self.main.pass_on_area()

        p_h = self.cal.demand_calculator(area)

        self.cal.heatpump_selector(p_h)
        dist=self.cal.heat_exchanger(k[0],float(self.annual_cons.get()))
        self.area_hx.set(value=self.cal.A_ghe)
        self.dbnloops.set(value=dist)


#class that contains the frame of horizontal heat exchanger
class VerticalHE(ttk.Frame):
    def __init__(self,container,parent,*args,**kwargs):
        super().__init__(container)

        self["style"] = "Background.TFrame"
        number_frame = ttk.Frame(self, style="Background.TFrame")
        number_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        area_frame = ttk.Frame(self, style="Background.TFrame")
        area_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
        self.main = parent
        self.soil_type = tk.StringVar()
        self.len_hx=tk.StringVar()
        self.nof_hx=tk.StringVar()
        self.list_ok= bool()
        self.radio_ok=bool()
        self.no_hx_ok=bool()

        #title of the page
        greetings = ttk.Label(number_frame, text="Vertical Ground Heat Exchanger",
                              style="LabelText.TLabel")
        greetings.grid(row=0, column=0, padx=20, pady=20, sticky="W")
        nofhx_label = ttk.Label(number_frame, text="Enter the number of boreholes required",
                                style="LightText.TLabel")
        nofhx_label.grid(row=1, column=0, sticky="EW")
        area_output = ttk.Entry(number_frame, textvariable=self.nof_hx,
                                width=15, style="EntryStyle.TEntry")
        area_output.grid(row=1, column=1, sticky="W")
        area_output.bind("<Any-KeyPress>",lambda e:self.button_activator(3))

        selection_label = ttk.Label(area_frame, text="Select the Type of Soil",
                                    style="LightText.TLabel")
        selection_label.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        #retreiving data of abstraction coefficients of different soils
        ac = pd.read_csv('vertical_abs_coeff.csv', header=0)
        AC_dict = ac.to_dict(orient='records')

        soil = tuple()
        for i in range(len(AC_dict)):
            soil += (AC_dict[i]['Soil Type'],)

        #inserting soil types as list for selection
        selected_type = tk.StringVar(value=soil)
        self.types_box = tk.Listbox(area_frame, listvariable=selected_type,
                                    height=5, width=40,
                                    selectmode='browse')
        self.types_box.grid(row=2, column=0, sticky="EW")

        scrollbar = ttk.Scrollbar(area_frame, orient='vertical',
                                  command=self.types_box.yview)
        self.types_box['yscrollcommand'] = scrollbar.set

        scrollbar.grid(row=2, column=1, sticky='ns')
        area_frame.columnconfigure(1,weight=1)

        self.types_box.bind('<<ListboxSelect>>', lambda e: self.button_activator(1))

        #selection pane for selecting the annual usage in hours
        selection_label = ttk.Label(area_frame, text="Specify the usage in hours per year",
                                    style ="LightText.TLabel",justify="center")
        selection_label.grid(row=1, column=2,padx=20, sticky="E")

        self.annual_cons = tk.StringVar()
        annual_1800 = ttk.Radiobutton(area_frame, text="Annual usage of 1800 hours",
                                      value=1800, variable=self.annual_cons,
                                      style ="Radio.TRadiobutton",
                                      command=lambda: self.button_activator(2))
        annual_2400 = ttk.Radiobutton(area_frame, text="Annual usage of 2400 hours",
                                      value=2400, variable=self.annual_cons,
                                      style ="Radio.TRadiobutton",
                                      command=lambda: self.button_activator(2))
        annual_1800.grid(row=2, column=2, sticky="E")
        annual_2400.grid(row=3, column=2, sticky="E")

        #button for calculating the results
        self.save_button = ttk.Button(area_frame,
                                 text="Calculate",
                                 command=lambda: self.activate_v_selections(),
                                 style="ButtonColour.TButton",
                                 state='disabled')
        self.save_button.grid(row=4, column=2,pady =20,padx=30, sticky="E")

        second_frame = ttk.Frame(self, style="Background.TFrame")
        second_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")
        area_label = ttk.Label(second_frame,
                               text="Depth required for Borehole Heat Exchanger: ",
                               style="LightText.TLabel")
        area_label.grid(row=0, column=0, sticky="W")
        area_output = ttk.Label(second_frame, textvariable=self.len_hx,
                                style ="LightText.TLabel")
        area_output.grid(row=0, column=1, sticky="W")
        area_unit = ttk.Label(second_frame, text="m",
                              style="LightText.TLabel")
        area_unit.grid(row=0, column=2, sticky="W")

        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")

        for child in second_frame.winfo_children():
            child.grid_configure(padx=10, pady=10)

        back_button = ttk.Button(button_container,
                                 text="Back",
                                 cursor="hand2",
                                 command=lambda: parent.change_frame_name(3),
                                 style ="ButtonColour.TButton")
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    #function for checking if all the necessary values are entered
    def button_activator(self,val,*args):
        try:
            if val==1:
                self.list_ok=True
            elif val==2:
                self.radio_ok=True
            elif val==3:
                self.no_hx_ok=True

            if self.list_ok and self.radio_ok and self.no_hx_ok:
                self.save_button.config(state="active")
        except UnboundLocalError:
            pass

    #function for calling the calculation section of the program
    def activate_v_selections(self):
        k= self.types_box.curselection()
        self.soil_type.set(k[0])

        self.cal = Calculations()
        area = self.main.pass_on_area()

        p_h = self.cal.demand_calculator(area)

        self.cal.heatpump_selector(p_h)
        dist = self.cal.vertical_hx(k[0], float(self.annual_cons.get()))
        #tot_length=self.cal.total_length
        length=dist/float(self.nof_hx.get())
        self.len_hx.set(value=round(length,2))

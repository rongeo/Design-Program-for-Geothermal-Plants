import tkinter as tk
from tkinter import ttk
from baseframe import Introframe,EnergyDemand,get_g_area
from exchangers import HorizontalHE,PumpSelection,VerticalHE
from graphics import set_dpi_awarness,Colour

#to increase the graphical output
set_dpi_awarness()

#styling UI with colours
selected_colour= Colour()
#selecting colours for the UI
i=5
colour_primary=selected_colour.combinations[i]["colour_primary"]
colour_secondary=selected_colour.combinations[i]["colour_secondary"]
colour_light_background=selected_colour.combinations[i]["colour_light_background"]
colour_light_text=selected_colour.combinations[i]["colour_light_text"]
colour_dark_text=selected_colour.combinations[i]["colour_dark_text"]


#The main class
class Heatpump(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Title of the program
        self.title("Geothermal Plant Design ")
        self.columnconfigure(0, weight=1)
        self.iconbitmap('logo.ico')

        container = ttk.Frame(self)
        container.grid()

        #initializing the frames involved
        demand_frame = EnergyDemand(container, self)
        demand_frame.grid(row=0, column=0, sticky="NSEW")
        pump_frame= PumpSelection(container, self)
        pump_frame.grid(row=0, column=0, sticky="NSEW")
        horizontal_frame = HorizontalHE(container, self)
        horizontal_frame.grid(row=0, column=0, sticky="NSEW")
        vertical_frame = VerticalHE(container,self)
        vertical_frame.grid(row=0, column=0, sticky="NSEW")
        intro_frame = Introframe(container, self)
        intro_frame.grid(row=0, column=0, sticky="NSEW")

        #Storing frames in a dictionary
        self.frames = dict()
        self.frames[Introframe] = intro_frame
        self.frames[EnergyDemand] = demand_frame
        self.frames[HorizontalHE]= horizontal_frame
        self.frames[PumpSelection]=pump_frame
        self.frames[VerticalHE] = vertical_frame

        #Styling the UI
        style = ttk.Style(self)
        st=2        #changing 1 to 2 allows UI change
        if st==1:
            style.theme_use("clam")
            style.configure("Window.TFrame", background=colour_light_background)
            style.configure("Background.TFrame", background=colour_primary)
            style.configure("LabelText.TLabel",
                            background=colour_light_background,
                            foreground=colour_dark_text,
                            font="Helvetica 16"
                            )
            style.configure("LightText.TLabel",
                            background=colour_primary,
                            foreground=colour_light_text,
                            font="Arial 11"
                            )
            style.configure("ButtonColour.TButton",
                            background=colour_secondary,
                            foreground=colour_light_text,
                            font="Arial 11")
            style.configure("Radio.TRadiobutton",background=colour_primary,
                            foreground=colour_light_text,
                            font="Arial 11")
            style.configure("EntryStyle.TEntry",
                            background=colour_light_background,
                            foreground=colour_primary,
                            font="Arial 11")
            style.configure("ListStyle.TListbox",
                            background=colour_light_background,
                            foreground=colour_dark_text,
                            font="Arial 11")
            self["background"] = colour_primary
        elif st==2:
            container.tk.call('source', 'azure.tcl')
            container.tk.call("set_theme", "light")        #use 'dark' for dark theme
            style.configure("LabelText.TLabel",
                            background=colour_light_background,
                            foreground=colour_dark_text,
                            font="Helvetica 16")

    #function that shows current frame
    def show_frames(self, selected_frame):
        frame = self.frames[selected_frame]
        frame.tkraise()

    #function that passes area entered by user to different classes
    def pass_on_area(self):
        area=get_g_area()
        return area

    #function that changes frames for buttons
    def change_frame_name(self,i):
        if i==2:
            self.show_frames(EnergyDemand)
        elif i==3:
            self.show_frames(PumpSelection)
        elif i==4:
            self.show_frames(HorizontalHE)
        elif i==5:
            self.show_frames(VerticalHE)


# defining the object that runs with the main class
window= Heatpump()

window.mainloop()
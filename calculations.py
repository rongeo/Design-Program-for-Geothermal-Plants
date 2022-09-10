import tkinter as tk
from tkinter import ttk
import pandas as pd


class Calculations():
    def __init__(self, *args, **kwargs):
        super().__init__()

    #function for calculating the demand required by the house
    def demand_calculator(self,area):
        HC_area = 0.04
        # "HC_area - German standard heat consumption per unit area [KW/m^2]"
        P_hg = area * HC_area
        # "P_hg - heat output generated"

        P_hwp = 0.3
        N = 4
        P_hw = P_hwp * N
        # "P_hw - heat output for hot water generation [KW]"
        # "P_hwp - heat output for hot water per person , 0.25 kw/person to 0.35 kw/ person"
        # "N - no of people"

        P_h_1 = P_hg + P_hw

        t_off = 4
        S_h = 24 / (24 - t_off)
        self.P_h = P_h_1 * S_h
        # "S_h = 24 h access period differences"
        # "t_off - blocking time in hours [h]"
        # "P_h - heat output considering blocking periods"

        return round(self.P_h, 2)

    #function for selecting a demo pump from the database of the pumps
    def heatpump_selector(self, P_h_new):

        df = pd.read_csv('heatpump_prop.csv', header=None)
        df = df.iloc[:, 0].str.split(',', n=0, expand=True)
        df.rename({0: 'Type', 1: 'TypeNo', 2: 'Heatoutput', 3: 'Poweroutput', 4: 'Unit', 5: 'COP'},
                  axis='columns',inplace=True)

        self.HP_dict = df.to_dict(orient='records')

        count = 0
        for i in range(len(self.HP_dict)):
            if P_h_new > float(self.HP_dict[i]['Heatoutput']):
                count = i
        count += 1

        #"Selecting a pump from manual"
        self.COP_hp=float(self.HP_dict[count]['COP'])
        self.P_e_cons=float(self.HP_dict[count]['Poweroutput'])
        self.P_h_p=float(self.HP_dict[count]['Heatoutput'])
        self.name=self.HP_dict[count]['Type'] + self.HP_dict[count]['TypeNo']

        self.P_c = self.P_h_p *(1-1/ self.COP_hp)

        # "Pc - cooling capacity in KW"
        # "Pe_cons - power consumption in KW"
        # "COP_hp - rated COP of HP as in manual"

    #function for calculating the area required for horizontal heat exchanger
    def heat_exchanger(self,soil_index,usage):

        ac = pd.read_csv('abstraction_coeff.csv', header=0)
        AC_dict = ac.to_dict(orient='records')

        if usage==1800:
            P_c_spec= float(AC_dict[soil_index]['Mean AC 1800h/a'])
        elif usage==2400:
            P_c_spec = float(AC_dict[soil_index]['Mean AC 2400h/a'])

        area=self.P_c / (P_c_spec * 0.001)
        self.A_ghe = round(area,2)


        # "Converting W to KW"
        # "A_ghe - area covered by ground heat exchangers in m2"
        # "P_c_spec - area specific abstraction capacity "
        # P_c_spec -[W / m ^ 2] "From VDI 4640 table"

        d_l18 = round(1.17 - P_c_spec * 0.017,2)
        d_l24 = round(1.17 - P_c_spec * 0.021,2)
        #
        # "d_l18 - max distance bn loops for an operating time of 1800h/a "
        # "d_l24 - max distance bn loops for an operating time of 2400h/a "

        if usage ==1800:
           return(d_l18)
        elif usage==2400:
            return(d_l24)

    #function for calculating the area required for vertical heat exchanger
    def vertical_hx(self,soil_index,usage):

        ac = pd.read_csv('vertical_abs_coeff.csv', header=0)
        AC_dict = ac.to_dict(orient='records')
        #reading abstraction coefficient from csv file- VDI4650

        if usage == 1800:
            P_c_spec = float(AC_dict[soil_index]['Mean AC 1800h/a'])
        elif usage == 2400:
            P_c_spec = float(AC_dict[soil_index]['Mean AC 2400h/a'])

        self.total_length=self.P_c *1000/P_c_spec
        #converting KW to W and finding the total length by dividing with abstraction capacity

        return self.total_length
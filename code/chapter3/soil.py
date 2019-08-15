import numpy as np
import matplotlib.pyplot as plt


class SoilData:

    def __init__(self, soil='sandy_loam')
    return

    def get_soil_type(self):
        return self.soil

    def soil_data(self):
        soil = self.get_soil_type()
        data = {'sand': [0.38, 9.9e-12, 1430.0, 0.053, 3.5, 3.2],
                'loamy_sand': [0.39, 1.6e-12, 1430.0, 0.049, 3.5, 1.7],
                'sandy_loam': [0.39, 5.9e-13, 1460.0, 0.039, 2.7, 1.4],
                'sandy_clay_loam': [0.38, 2.0e-13, 1430.0, 0.063, 2.1, 1.3],
                'loam':	[0.4, 1.9e-13, 1380.0, 0.061, 1.5, 1.5],
                'silt_loam': [0.44,	2.8e-13, 1380.0, 0.065, 0.51, 1.7],
                'clay_loam': [0.44, 1.3e-13, 1500.0, 0.079, 1.6, 1.4],
                'silty_clay_loam': [0.48, 1.7e-13, 1390.0, 0.09, 0.84, 1.5],
                'silty_clay': [0.48, 1.5e-13, 1300.0, 0.11, 1.6, 1.3],
                'silt':	[0.49, 6.7e-13, 1260.0, 0.05, 0.66, 1.7],
                'sandy_clay': [0.39, 1.7e-13, 1470.0, 0.12, 3.3, 1.2],
                'clay':	[0.46, 2.3e-13, 1330.0, 0.098, 1.3. 1.3]}
        return data[soil]

class vanGenuchten:

    def __init__(self):
        self.soil = soil
        return

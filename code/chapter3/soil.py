import numpy as np
import matplotlib.pyplot as plt


class Soil:
    def __init__(self, soil_type):
        self.set_soil_type(soil_type)
        self.set_soil_data()
        return

    def set_soil_type(self, soil_type):
        self.soil_type = soil_type
        return
    def get_soil_type(self):
        return self.soil_type

    def set_soil_data(self):
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
                'clay':	[0.46, 2.3e-13, 1330.0, 0.098, 1.3, 1.3]}
        self.epsilon = data[soil][0]
        self.kappa = data[soil][1]
        self.rho = data[soil][2]
        self.theta_r = data[soil][3]
        self.alpha = data[soil][4]
        self.n = data[soil][5]
        self.m = 1-1/self.n
        self.l = 0.5
        return

    def get_porosity(self):
        return self.epsilon
    def get_permeability(self):
        return self.kappa
    def get_density(self):
        return self.rho
    def get_residual_moisture(self):
        return self.theta_r
    def get_alpha(self):
        return self.alpha
    def get_n(self):
        return self.n
    def get_m(self):
        return self.m
    def get_l(self):
        return self.l

    def get_soil_data(self):
        data = {'porosity': self.get_porosity(), 'permeability': self.get_permeability(),
        'density': self.get_density(), 'residual_moisture': self.get_residual_moisture(),
        'alpha': self.get_alpha(), 'n': self.get_n(), 'm': self.get_m()}
        return data


class vanGenuchten(Soil):
    """
    Calculates the soil liquid saturation based on the pressure head according
    to the van Genuchten retention model. A pressure head that is zero or positive gives by definition
    fully saturated soil. A negative pressure head gives a variable saturation.

    Arg:
        pressure_head: pressure head (m)
    Return:
        Se: soil moisture saturation
    """
    def get_saturation(self,pressure_head):
        Se = []
        for Hp in pressure_head:
            if Hp >= 0:
                Se.append(1)
            elif Hp < 0:
                alpha = self.get_alpha()
                n = self.get_n()
                m = self.get_m()
                Se.append(1/(1+abs(alpha*Hp)**n)**m)
        return np.array(Se)
    """
    Returns the soil liquid content based on the saturation.
    """
    def get_liquid_content(self,Hp):
        Se = self.get_saturation(Hp)
        epsilon = self.get_porosity()
        theta_r = self.get_residual_moisture()
        return theta_r+Se*(epsilon-theta_r)
    """
    Returns the soil liquid content based on the soil liquid content.
    """
    def get_gas_content(self, Hp):
        epsilon = self.get_porosity()
        theta = self.get_liquid_content(Hp)
        return epsilon-theta

    def get_liquid_capacity(self,Hp):
        alpha = self.get_alpha()
        m = self.get_m()
        epsilon= self.get_porosity()
        theta_r = self.get_residual_moisture()
        Se = self.get_saturation(Hp)
        return alpha*m/(1-m)*(epsilon-theta_r)*Se**(1/m)*(1-Se**(1/m))**m

    def get_relative_permeability(self,Hp):
        m = self.get_m()
        l = self.get_l()
        Se = self.get_saturation(Hp)
        return Se**l*(1-(1-Se)**(1/m))**2

class Contaminant:
    def __init__(self, contaminant):
        self.set_contaminant(contaminant)
        self.set_contaminant_data()
        return

    def set_contaminant(self,contaminant):
        self.contaminant = contaminant
        return

    def get_contaminant(self):
        return self.contaminant

    def set_contaminant_data(self):
        contaminant = self.get_contaminant()
        # M, K_H, D_air, D_water
        # TODO: Fix these values
        data = {'TCE': [131.38, 0.4, 7.4e-6, 1e-9]}

        self.M = data[contaminant][0]
        self.K_H = data[contaminant][1]
        self.D_air = data[contaminant][2]
        self.D_water = data[contaminant][3]
        return

    def get_molar_mass(self):
        return self.M
    def get_henrys_constant(self):
        return self.K_H
    def get_air_diffusion_coeff(self):
        return self.D_air
    def get_water_diffusion_coeff(self):
        return self.D_water

class MillingtonQuirk(vanGenuchten,Contaminant):
    def __init__(self, soil_type, contaminant):
        vanGenuchten.__init__(self,soil_type)
        Contaminant.__init__(self,contaminant)
        return

    def get_effective_diffusion_coeff(self,pressure_head):
        D_air = self.get_air_diffusion_coeff()
        D_water = self.get_water_diffusion_coeff()
        K_H = self.get_henrys_constant()
        theta = self.get_liquid_content(pressure_head)
        theta_g = self.get_gas_content(pressure_head)
        epsilon = self.get_porosity()
        return D_water*theta**(10/3)/epsilon**2+D_air/K_H*theta_g**(10/3)/epsilon**2


# TODO: Make the plot... and probably make sure calculations are OK
z = np.linspace(0, -4)
diff = MillingtonQuirk('sand', 'TCE')

fig, ax = plt.subplots(dpi=300)

ax.semilogx(diff.get_effective_diffusion_coeff(z),-z)
plt.show()

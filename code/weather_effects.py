import numpy as np
import matplotlib.pyplot as plt

class AirExchangeRate:
    """
    Estimates the air exchange rate (Ae) of a building, based on the Dietz et al. 1986
    model for estimating Ae.
    """
    def __init__(self, L=3, C=5):
        self.L = L
        self.C = C

        return



    def get_leakiness(self):
        return self.L

    def get_sheltering(self):
        return self.C
    def get_air_exchange_rate(self, dT, U):
        L = self.get_leakiness()
        C = self.get_sheltering()
        return L*(0.006*dT+0.03/C*U**1.5)


x = AirExchangeRate()

dT = np.linspace(-20,20, 100)
U = np.linspace(0,10)


fig, (ax1, ax2) = plt.subplots(2,1,dpi=300)

ax1.plot(dT, x.get_air_exchange_rate(dT,0))
ax2.plot(U, x.get_air_exchange_rate(0,U))


plt.show()

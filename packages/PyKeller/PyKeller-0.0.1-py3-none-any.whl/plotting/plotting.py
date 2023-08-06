#Created: Sat Aug  3 20:30:50 2019
#By: mach

import matplotlib.pyplot as plt
import PyKeller.signal_processing.signal_analysis as sa

def plot_bar(bins,hist):
    
    bins_mid = sa.midpoint(bins)
    plt.bar(bins_mid,hist)
    plt.show()
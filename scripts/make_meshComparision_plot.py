#!/usr/bin/env python

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():

    # (countRatio, resolutionRatio, speedup)
    ltsExperimentData = [(0.164, 32, -1.497),
                         (0.258, 32, 8.882),
                         (0.462, 32, 29.528),
                         (1.050, 32, 45.326),
                         (1.863, 32, 59.428),
                         (2.652, 32, 63.964),
                         (4.018, 32, 66.170),
                         (6.627, 32, 68.947),
                         (11.907, 32, 69.453),
                         (16.460, 32, 67.989),
                         (23.004, 32, 71.394),
                         (1.040, 1, -108.442),
                         (1.040, 2, -29.859),
                         (0.956, 4, 8.635),
                         (1.025, 8, 30.337),
                         (0.994, 16, 38.782),
                         (1.017, 32, 49.801),
                         (0.955, 64, 54.045)]

    # trim certain points so plot is balanced
    ltsExperimentData.remove((0.955, 64, 54.045))
    ltsExperimentData.remove((16.460, 32, 67.989))
    ltsExperimentData.remove((23.004, 32, 71.394))
    ltsExperimentData.remove((1.040, 1, -108.442))

    countRatios = []
    resolutionRatios = []
    speedups = []
    for point in ltsExperimentData:
        countRatios.append(point[0])
        resolutionRatios.append(point[1])
        speedups.append(point[2])


    plt.scatter(countRatios, resolutionRatios, c=speedups, s=400)
    plt.xlabel('countRatio')
    plt.ylabel('resolutionRatio')
    
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('% speedup')

    # MPAS meshes
    
    # SOwISC12to60E2r4
    plt.scatter(4.343, 5, c=0 , s=50, cmap='spring', label='SOwISC12to60E2r4')
    
    # ARRM60to10
    plt.scatter(5.120, 6, c=0 , s=50, cmap='summer', label='ARRM60to10')
    
    # ARRM60to6
    plt.scatter(1.913, 10, c=0 , s=50, cmap='autumn', label='ARRM60to6')
    
    # WC14to60E2r3
    plt.scatter(0.869, 4.286, c=0 , s=50, cmap='winter', label='WC14to60E2r3')
    
    # WCAtl12to45E2r4
    plt.scatter(1.900, 3.75, c=0 , s=50, cmap='cool', label='WCAtl12to45E2r4')
    
    # delawareBay
    plt.scatter(0.788, 32, c=0 , s=50, cmap='gray', label='delawareBay2.5to80')

    plt.legend()

    plt.title('MPAS-Meshes compared to SW LTS Experiments')
    
    plt.savefig('meshComparison.png', bbox_inches='tight')

# END main()


if __name__ == '__main__':
    # if run as primary module call main
    main()


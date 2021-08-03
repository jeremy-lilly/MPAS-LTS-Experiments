#!/usr/bin/env python


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset


def main():

    testDirs = [sub for sub in os.listdir('.') if (os.path.isdir(sub) and 'rk4' not in sub)]
    operators = ['u', 'h']

    nTests = len(testDirs)
    nOperators = len(operators)
    difl2 = np.zeros([nOperators, nTests])

    refSolFile = Dataset('./refSol_rk4_01/output.nc', 'r')

    data = []

    for testDir in testDirs:
        with open('./' + testDir + '/namelist.sw') as namelistFile:
            namelistTxt = namelistFile.read().split('\n')
            for line in namelistTxt:
                if 'config_dt = ' in line:
                    dt = float(line.split()[-1])
                elif 'config_dt_scaling_LTS = ' in line:
                    M = int(line.split()[-1])
            # END for
        # END with

        with open('./' + testDir + '/log.sw.0000.out') as logFile:
            for line in logFile.read().split('\n'):
                words = line.split()
                if 'time' and 'integration' in words:
                    time = float(words[3])

        # END with

        data.append((dt, testDir, time, M))

    # END for

    data.sort()
    coarseDTs = [dat[0] for dat in data]
    testDirs = [dat[1] for dat in data]
    times = [dat[2] for dat in data]
    Ms = [dat[3] for dat in data]

    print(coarseDTs)


    tableData = np.matrix([Ms,
                           coarseDTs,
                           times])

    pltFig, pltAx = plt.subplots(1, 1, figsize=(16, 9))
    tblFig, tblAx = plt.subplots(1, 1, figsize=(16, 9))
   
    for iOp, operator in enumerate(operators):
        refSol = refSolFile.variables[operator][1, :, 0]
        refSolNorm = np.sqrt(np.sum(refSol**2))

        for iCase, testDir in enumerate(testDirs):
            solFile = Dataset(testDir + '/output.nc', 'r')
    
            sol = solFile.variables[operator][1, :, 0]

            dif = abs(sol - refSol)
            difSquared = dif**2
            difl2[iOp, iCase] = np.sqrt(np.sum(difSquared[:])) / refSolNorm

            solFile.close()

        pltAx.plot(coarseDTs, difl2[iOp, :], '-o',
                   label=operators[iOp])
        tableData = np.vstack([tableData, difl2[iOp, :]])
        print(difl2[iOp, :])

        # END for

    #END for

    refSolFile.close()


    tableData = tableData.transpose()

    tblLabels = ['M', 'coarseDT (s)', 'CPU-time for time integration (s)']
    for operator in operators:
        tblLabels.append('Relative l2 error in ' + operator)
    
    figSupTitle = 'Convergence in coarseDT of relative l2 error'
    figTitle = 'fineDT = 10.0, runTime = 01:00:00'

    pltAx.grid()
    pltAx.legend()
    pltAx.set(xlabel='coarseDT',
              ylabel='Relative l2 error',
              title=figTitle)
    pltFig.suptitle('Convergence in coarseDT of relative l2 error')

    tblAx.axis('off')
    tblAx.axis('tight')
    dataFrame = pd.DataFrame(tableData, columns=tblLabels)
    table = tblAx.table(cellText=dataFrame.values, colLabels=dataFrame.columns, loc='center')
    table.scale(1, 3)
    tblAx.set(title=figTitle)
    tblFig.suptitle(figSupTitle)

    pltFig.savefig('convergenceInM_plot.png', bbox_inches='tight')
    tblFig.savefig('convergenceInM_table.png', bbox_inches='tight')

# END main()


if __name__ == '__main__':
    # if run as primary  modul call main 
    main()


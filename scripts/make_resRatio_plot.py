#!/usr/bin/env python

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():

    data = []

    testdirs =  [sub for sub in os.listdir('.') if os.path.isdir(sub)]

    for testdir in testdirs:
        if not 'rk4' in testdir:
        
            with open('./' + testdir + '/log.sw.0000.out') as logf, \
                 open('./' + testdir + '/parameterList.txt') as paraf:

                for line in logf.read().split('\n'):
                    words = line.split()
                    if 'time' and 'integration' in words:
                        timeLTS = float(words[3])
                
                for line in paraf.read().split('\n'):
                    words = line.split()
                    if 'Ratio' in words and 'fineRes' in words:
                        resRatio = float(words[-1])
                    elif 'Ratio' in words and 'number' in words:
                        numRatio = float(words[-1])
                    elif 'coarseDT' in words:
                        coarseDT = float(words[-1])
                    elif 'fineM' in words:
                        fineM = float(words[-1])
                    elif 'fineRes' in words:
                        fineRes = float(words[-1])

                with open('./' + testdir + '_rk4' + '/log.sw.0000.out') as rk4Logf, \
                     open('./' + testdir + '_rk4' + '/parameterList.txt') as rk4Paraf:
                    for line in rk4Logf.read().split('\n'):
                        words = line.split()
                        if 'time' and 'integration' in words:
                            timeRK4 = float(words[3])
                    
                    for line in rk4Paraf.read().split('\n'):
                        words = line.split()
                        if 'coarseDT' in words:
                            rk4DT = float(words[-1])


                data.append((resRatio, numRatio, fineRes, timeLTS, timeRK4, coarseDT, fineM, rk4DT))
            
            # END with

        # END if  
    # END for

    data.sort()

    resRatio = np.array([dat[0] for dat in data])
    numRatio = np.array([dat[1] for dat in data])
    fineRes = np.array([dat[2] for dat in data])
    timeLTS = np.array([dat[3] for dat in data])
    timeRK4 = np.array([dat[4] for dat in data])
    coarseDT = np.array([dat[5] for dat in data])
    fineM = np.array([dat[6] for dat in data])
    rk4DT = np.array([dat[7] for dat in data])
    
    speedup = ((timeRK4 - timeLTS) / timeRK4) * 100
    fineDT = coarseDT / fineM
    dtRatio = rk4DT / fineDT

    tableData = np.matrix([resRatio,
                           speedup,
                           fineRes,
                           numRatio,
                           coarseDT,
                           fineDT,
                           rk4DT,
                           dtRatio]).transpose()
    
    pltFig, pltAx = plt.subplots(1, 1)
    tblFig, tblAx = plt.subplots(1, 1)

    figSupTitle = 'Effect of the ratio of coarse resolution to fine resolution on speedup'
    figTitle = 'coarseRes = 80.0 km, numInterface = 25, nVertLevels = 100, runTime = 00:30:00'

    pltAx.plot(resRatio, speedup, 'o-')
    pltAx.grid(which='major')
    pltAx.set(xlabel='coarseResolution / fineResolution',
              ylabel='% speedup of LTS3 over RK4',
              title=figTitle)
    pltFig.suptitle(figSupTitle)

    tblAx.axis('off')
    tblAx.axis('tight')
    dataFrame = pd.DataFrame(tableData, columns=['coarseResolution\n/ fineResolution',
                                                 '% speedup',
                                                 'fineRes (km)',
                                                 'nCoarseCells\n/ nFineCells',
                                                 'coarseDT (s)',
                                                 'fineDT (s)',
                                                 'rk4DT (s)',
                                                 'rk4DT\n/ fineDT'])
    table = tblAx.table(cellText=dataFrame.values,
                        colLabels=dataFrame.columns,
                        loc='center')
    table.scale(1, 2)
    tblAx.set(title=figTitle)
    tblFig.suptitle(figSupTitle)
   
    pltFig.set_size_inches(16, 9)
    tblFig.set_size_inches(16, 9)

    ratio = 9 / 16
    pltAx.set_aspect(1.0 / pltAx.get_data_ratio() * ratio)
    tblAx.set_aspect(1.0 / tblAx.get_data_ratio() * ratio)

    pltFig.savefig('resRatio_speedup_plot.png')
    tblFig.savefig('resRatio_speedup_table.png')
    
# END main()


if __name__ == '__main__':
    # if run as primary module call main
    main()


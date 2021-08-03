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
                    if 'Ratio' and 'number' in words:
                        ratio = float(words[-1])
                    elif 'fineRadius' in words:
                        radius = float(words[-1])
                    elif 'Number' and 'cells' and 'fine' in words:
                        nFine = int(words[-1])

                with open('./' + testdir + '_rk4' + '/log.sw.0000.out') as rk4Logf:
                    for line in rk4Logf.read().split('\n'):
                        words = line.split()
                        if 'time' and 'integration' in words:
                            timeRK4 = float(words[3])


                data.append((ratio, timeLTS, timeRK4, radius, nFine))
            
            # END with

        # END if
    
    # END for

    data.sort()

    ratio = np.array([dat[0] for dat in data])
    timeLTS = np.array([dat[1] for dat in data])
    timeRK4 = np.array([dat[2] for dat in data])
    radius = np.array([dat[3] for dat in data])
    nFine = np.array([dat[4] for dat in data])
    
    speedup = ((timeRK4 - timeLTS) / timeRK4) * 100

    print(ratio)
    print(timeLTS)
    print(timeRK4)
    print(speedup)
    print(radius)
    print(nFine)

    tableData = np.matrix([ratio,
                           speedup,
                           nFine]).transpose()
    
    pltFig, pltAx = plt.subplots(1, 1, figsize=(16, 9))
    tblFig, tblAx = plt.subplots(1, 1, figsize=(16, 9))
    
    figSupTitle = 'Effect of the ratio of the number of coarse cells to number of fine cells on speedup'
    figTitle = 'nCoarseCells = 91,600 +/- 30, numInterface = 25, nVertLevels = 100, runTime = 00:30:00'

    pltAx.plot(ratio, speedup, 'o-')
    pltAx.grid(which='major')
    pltAx.set(xlabel='nCoarseCells / nFineCells',
              ylabel='% speedup of LTS3 over RK4',
              title=figTitle)
    pltFig.suptitle(figSupTitle)

    tblAx.axis('off')
    tblAx.axis('tight')
    dataFrame = pd.DataFrame(tableData, columns=['nCoarseCells / nFineCells',
                                                 '% speedup',
                                                 'nFineCells'])
    table = tblAx.table(cellText=dataFrame.values, colLabels=dataFrame.columns, loc='center')
    table.scale(1, 2)
    tblAx.set(title=figTitle)
    tblFig.suptitle(figSupTitle)

    pltFig.savefig('countRatio_speedup_plot.png', bbox_inches='tight')
    tblFig.savefig('countRatio_speedup_table.png', bbox_inches='tight')
    
# END main()


if __name__ == '__main__':
    # if run as primary module call main
    main()


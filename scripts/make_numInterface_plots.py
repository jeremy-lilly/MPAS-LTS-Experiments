#!/usr/bin/env python

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from math import ceil


def main():
    
    interfaceTests = [sub for sub in os.listdir('.') if os.path.isdir(sub)]
    procTests = [filename.split('.')[-1] for filename in os.listdir(interfaceTests[0]) if 'log.sw.0000.out.' in filename]

    interfaceTests.sort(key=int)
    procTests.sort(key=int)

    interfaceTestsInts = [int(test) for test in interfaceTests]
    procTestsInts = [int(test) for test in procTests]

    nInterfaceTests = len(interfaceTests)
    nProcTests = len(procTests)

    print(interfaceTests)
    print(procTests)

    
    # axis 0 = interfaceTest, axis 1 = procTest
    timeIntData = np.zeros([nInterfaceTests, nProcTests])

    for iInterface, interfaceTest in enumerate(interfaceTests):
        for iProc, procTest in enumerate(procTests):
            
            with open('./' + interfaceTest + '/log.sw.0000.out.' + procTest) as logf:
                for line in logf.read().split('\n'):
                    words = line.split()
                    if 'time' and 'integration' in words:
                        timeIntData[iInterface, iProc] = float(words[3])
                # END for
            # END with

        # END for
    # END for

    print(timeIntData)


    # scaling plots
    scaleFig, scaleAxes = plt.subplots(ceil(nInterfaceTests / 3), 3,
                                       sharey='all', sharex='all')
    scaleAxes = np.ravel(scaleAxes)
    
    perfectScaling = [10**4 / num for num in procTestsInts]

    for iInterface, interfaceTest in enumerate(interfaceTests):
        ax = scaleAxes[iInterface]
        ax.loglog(procTestsInts, timeIntData[iInterface, :], '-o')
        ax.loglog(procTestsInts, perfectScaling, '--', color='black')
        ax.grid('both')
        ax.set(title=('numInterface = ' + interfaceTest),
               xlabel='nProcs',
               ylabel='runtime (s)')
    # END for

    if nInterfaceTests % 3 == 2:
        scaleFig.delaxes(scaleAxes[-1])
    elif nInterfaceTests % 3 == 1:
        scaleFig.delaxes(scaleAxes[-1])
        scaleFig.delaxes(scaleAxes[-2])

    scaleFig.set_tight_layout(True)
    scaleFig.savefig('numInterface_scaling_plot.png', bbox_inches='tight')


    # interface runtime plots
    runtimeFig, runtimeAxes = plt.subplots(ceil(nProcTests / 2), 2,
                                           figsize=(6, 7))
    runtimeAxes = np.ravel(runtimeAxes)
    
    for iProc, procTest in enumerate(procTests):
        ax = runtimeAxes[iProc]
        print(timeIntData[:, iProc])
        ax.plot(interfaceTestsInts, timeIntData[:, iProc], '-o')
        ax.grid('major')
        ax.set(title=('numProcs = ' + procTest),
               xlabel='numInterface',
               ylabel='runtime (s)')
    # END for
    
    if nProcTests % 2 == 1:
        runtimeFig.delaxes(runtimeAxes[-1])
    
    runtimeFig.set_tight_layout(True)
    runtimeFig.savefig('numInterface_runtime_plot.png', bbox_inches='tight')
# END main()


if __name__ == '__main__':
    # if run as primary module call main
    main()

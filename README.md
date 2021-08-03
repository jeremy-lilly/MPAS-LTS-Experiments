# MPAS-LTS-Experiments

Proceedings from the 2021 PCSRI at LANL: Four experiments related to the performance and accuracy of local time-stepping (LTS) schemes as applied to the shallow water core of MPAS-Ocean.

******

## Parameters

Here we describe the parameters referenced by the [script](https://github.com/jeremy-lilly/MPAS-Model/blob/local_time_stepping_rebase/testing_and_setup/sw/lts/build_test5.py) used to generate the test cases described below.

- `numProcs`: (int) The number of MPI ranks to run the model with.
- `multiBlocksPerProc`: (bool) Whether or not to partition the graph so that each MPI rank owns three blocks -- one for each type of LTS cell (fine, coarse, and interface).
- `numInterfaceLayers`: (int) The number of interface layers.
- `coarseRegionDist`: (float) The angle in radians measured from the mountain from test case 5 in Williamson et al. where the coarse region starts.
- `coarseDT`: (float) The time-step to use on the coarse region.
- `fineM`: (int) The factor `M` that defines `fineDT = coarseDT / M`.
- `coarseRes`: (float) The target cell width in kilometers for large cells.
- `fineRes`: (float) The target cell width in kilometers for small cells.
- `fineRadius`: (float) The radius of a circle in kilometers to place cells of with width given by `fineRes` in around the mountain. Cells outside this circle will have width given by `coarseRes`.
- `runtime`: (hh:mm:ss) The length of time to run the simulation.
- `nVertLevels`: (int) The number of vertical layers in the model.

**Note:** Cells that have width given by `coarseRes` are not nessecarily "coarse cells" in that the coarse time-step is used on them. The cells labels (fine, coarse, interface) are defined exclusively by `coarseRegionDist` and `numInterfaceLayers`, whereas the cells physical sizes and locations are defined by `coarseRes`, `fineRes`, and `fineRadius`. For example, one can have cells that have width given by `coarseRes`, but lie within the fine region and are therefore labeled as fine cells.

## Experiments

For reproducibility, we provide a description of the methodology of each experiment. The meshs used in each test case for each experiment are based off of test case 5 from Williamson et al. and  were generated using [this script](https://github.com/jeremy-lilly/MPAS-Model/blob/local_time_stepping_rebase/testing_and_setup/sw/lts/build_test5.py).

### `countRatio` Experiment

The purpose of this experiment is to see how LTS3 performs compared to RK4 as we change the ratio of number of coarse cells to number of fine cells (`countRatio = nCoarseCells / nFineCells`). In order to vary `countRatio`, we fix a number of coarse cells and add more fine cells to the mesh by increasing `fineRadius`. Note that in practice, the number of coarse cells cannot be fixed as it is not directly controlled by the user -- rather it is determined by by the mesh generation software. We can however roughly "fix" this value by holding `coarseRegionDist` fixed.

**Note:** Since we are "fixing" `coarseRegionDist` and varying `fineRadius`, in each test mesh we will have "large" cells that are labeled as fine. This does not effect the results of the experiment since these "large" fine cells require the same amount of work as a "small" fine cell and are counted as a fine cell in `nFineCells`. In the other experiments described here, we set `coarseRegionDist` intentionally to minimize the number of "large" fine cells.

#### Methodology

Run LTS3 and RK4 on the same meshes as we vary the value of `fineRadius` and plot `speedup = ( (timeRK4 - timeLTS3) / timeRK4 ) * 100` against `countRatio = nCoarseCells / nFineCells`. Each test case was generated with a different value of `fineRadius`.

Each LTS3 test case was generated with a command of the form:
```
./build_test5.py --disable-output -k -l 25 -f 2.5 -c 80 -d 200 -M 25 -r /path/to/MPAS-Model/repo -o /path/to/output/directory/FINE_RADIUS -s FINE_RADIUS
```
Each corresponding RK4 test case was generated with a command of the form:
```
./build_test5.py --disable-output --rk4 -d 12 -f 2.5 -c 80 -r /path/to/MPAS-Model/repo -o /path/to/output/directory/FINE_RADIUS_rk4 -s FINE_RADIUS
```

In this way, each test case sits in its own directory within a single parent directory (this is the expected directory structure for running `make_countRatio_plot.py` from this shared parent directory):
```
/countRatio
    /250        /300        ...
    /250_rk4    /300_rk4    ...
    /275        /350        ...
    /275_rk4    /350_rk4    ...
```

##### Generating Data

From each test case directory:
```
mpirun -n 128 sw_model namelist.sw streams.sw
```

##### Fixed Parameters:

- `numProcs = 128`
- `multiBlocksPerProc = True`
- `numInterfaceLayers = 25`
- `coarseRegionDist = 0.55`
- `coarseDT = 200`
- `fineM = 25`
- `coarseRes = 80`
- `fineRes = 2.5`
- `runtime = 00:30:00`
- `nVertLevels = 100`

##### Test Cases

| `fineRadius` |
| - |
| 250 |
| 275 |
| 300 |
| 350 | 
| 400 |
| 450 |
| 500 |
| 600 |
| 800 |
| 1000 |
| 1200 |

### `resolutionRatio` Experiment

The purpose of this experiment was to see see how LTS3 performs compared to RK4 as we change the ratio of number of coarse cells to number of fine cells (`resolutionRatio = coarseRes / fineRes`). In order to vary `resolutionRatio`, we fix `coarseRes` and vary `fineRes`. A tricky aspect of this experiment is that when we change these parameters, `countRatio` also changes. We saw in the previous experiment that this parameter does effect speedup, so in order for each `resolutionRatio` test case to be comparable to the others, we do our best hold `countRatio` fixed by carefully setting `coarseRegionDist` and `fineRadius`.

The coarse/fine time-steps for LTS3 and the global time steps for RK4 depend on `coarseRes` and `fineRes`. For each test case, we experimentally found the largest time-steps for which the corresponding methods were stable by simply increasing the values until the solution given by the model blew up. In each case, the RK4 time-step is roughly 1.5 times the fine time-step.

#### Methodology

Run LTS3 and RK4 on the same meshes as we vary the value of `fineRes` and plot `speedup = ( (timeRK4 - timeLTS3) / timeRK4 ) * 100` against `resolutionRatio = coarseRes / fineRes`.

Each LTS3 test case was generated with a command of the form:
```
./build_test5.py --disable-output -c 80 -k -l 25 -d 225 -r /path/to/MPAS-Model/repo -o  /path/to/output/directory/FINE_RES -f FINE_RES -s FINE_RADIUS -e COARSE_REGION_DIST -M FINE_M
```
Each corresponding RK4 test case was generated with a command of the form:
```
./build_test5.py --disable-output --rk4 -c 80 -r /path/to/MPAS-Model/repo -o /path/to/output/directory/FINE_RES_rk4 -f FINE_RES -s FINE_RADIUS -d RK4DT
```

In this way, each test case sits in its own directory within a single parent directory (this is the expected directory structure for running `make_resRatio_plot.py` from this shared parent directory):
```
/resolutionRatio
    /1.25       /5          ...
    /1.25_rk4   /5_rk4      ...
    /2.5        /10         ...
    /2.5_rk4    /10_rk4     ...
```

##### Generating Data

From each test case directory:
```
mpirun -n 128 sw_model namelist.sw streams.sw
```

##### Fixed Parameters:
- `numProcs = 128`
- `multiBlocksPerProc = True`
- `numInterfaceLayers = 25`
- `coarseDT = 225`
- `coarseRes = 80`
- `runtime = 00:30:00`
- `nVertLevels = 100`

##### Test Cases

| `fineRes` | `fineRadius` | `coarseRegionDist` | `fineM` | `RK4DT` |
| - | - | - | - | - |
| 80 | 400 | 1.85 | 1 | 360 |
| 40 | 5700 | 1.25 | 2 | 180 |
| 20 | 3250 | 0.85 | 4 | 93 |
| 10 | 1700 | 0.6 | 8 | 45 |
| 5 | 975 | 0.52 | 14 | 25 |
| 2.5 | 610 | 0.45 | 26 | 12 |
| 1.25 | 450 | 0.43 | 50 | 6 |

### `numInterfaceLayers` Experiment

The purpose of this experiment is to see how LTS3 scales across the number of MPI ranks for different values of `numInterfaceLayers`.

#### Methodology

Run LTS3 on the same mesh as we increase `numInterfaceLayers`, then run each of these cases with different numbers of MPI processors.

Test cases were generated with commands of the form:
```
./build_test5.py -f 2.5 -c 80 -d 200 -M 25 -k -s 600 -r /path/to/MPAS-Model/repo -o /path/to/output/directory/NUM_INTERFACE -l NUM_INTERFACE -e COARSE_REGION_DIST
```

Then, additional `graph.info.part.NUM_BLOCKS` files need to be generated for each test case directory by running the following (in each test case directory):
```
gpmetis graph.info NUM_BLOCKS
./build_graph_info_part_for_multi_block_run.py -k NUM_BLOCKS
```
**Note:** `NUM_BLOCKS = 3 * numProcs`.

In this way, each test case sits in its own directory within a single parent directory (this is the expected directory structure for running `make_numInterface_plots.py` from this shared parent directory):
```
/numInterface
    /1      /20     /40
    /5      /25     
    /10     /30     
    /15     /35     
```

##### Generating Data

From each test case directory (after generating the additional `graph.info.part.NUM_BLOCKS` files) and for each value of `numProcs` to test with, do:
```
# edit namelist.sw so that config_number_of_blocks = NUM_BLOCKS
mpirun -n NUM_PROCS sw_model namelist.sw streams.sw
mv log.sw.0000.out log.sw.0000.out.NUM_PROCS
```

##### Fixed Parameters

- `multiBlocksPerProc = True`
- `numInterfaceLayers = 25`
- `coarseDT = 200`
- `fineM = 25`
- `coarseRes = 80`
- `fineRes = 2.5`
- `fineRadius = 600`
- `runtime = 00:30:00`
- `nVertLevels = 100`

##### Test Cases

| `numInterfaceLayers` | `coarseRegionDist` |
| - | - |
| 1 | 0.17 |
| 5 | 0.21 | 
| 10 | 0.26 |
| 15 | 0.33 |
| 20 | 0.4 |
| 25 | 0.46 |
| 30 | 0.52 | 
| 35 | 0.58 | 
| 40 | 0.64 |

### Convergence in `fineM` Experiment

The purpose of this experiment was to see how the accuracy of the solution generated by LTS3 changes when we fix `fineDT = 10` and vary `fineM` so that `coarseDT` increases. The accuracy is then compared to a solution generated by RK4 with a time-step of 0.1 second.

#### Methodology

Each LTS3 test case was generated with a command of the form:
```
./build_test5.py -k -f 50 -c 400 -s 6000 -e 1.25 -t 01:00:00 -r /path/to/MPAS-Model/repo -o /path/to/output/directory/FINE_M -M FINE_M -d COARSE_DT
```

The RK4 reference solution test case was generated with:
```
./build_test5.py -f 50 -c 400 -s 6000 -d 0.1 -t 01:00:00 -r /path/to/MPAS-Model/repo -o /path/to/output/directory/refSol_rk4_01
```

In this way, each test case sits in its own directory within a single parent directory (this is the expected directory structure for running `make_convergenceInM_plot.py` from this shared parent directory):
```
/convergenceInM
    /refSol_rk4_01      /15
    /1                  /30
    /5                  /60
    /10                 /90
```

##### Generating Data

From each test case directory:
```
mpirun -n 128 sw_model namelist.sw streams.sw
```

##### Fixed Parameters

- `numProcs = 128`
- `multiBlocksPerProc = True`
- `numInterfaceLayers = 1`
- `coarseRegionDist = 1.25`
- `coarseRes = 80`
- `fineRes = 2.5`
- `runtime = 01:00:00`
- `nVertLevels = 100`

##### Test Cases

| `M` | `coarseDT` | 
| - | - |
| 1 | 10 | 
| 5 | 50 |
| 10 | 100 |
| 15 | 150 | 
| 30 | 300 | 
| 60 | 600 |
| 90 | 900 |


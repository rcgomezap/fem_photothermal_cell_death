# trace generated using paraview version 5.13.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3 Reader S'
txdmf = Xdmf3ReaderS(registrationName='T.xdmf', FileName=['/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_lopes_dp1/fenicsx/results/T.xdmf'])

UpdatePipeline(time=0.0, proxy=txdmf)

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(registrationName='PlotOverLine1', Input=txdmf)

# Properties modified on plotOverLine1
plotOverLine1.Point1 = [0.0, 0.03999999910593033, 0.0]
plotOverLine1.Point2 = [0.0, 0.0, 0.0]

UpdatePipeline(time=710.0, proxy=plotOverLine1)

# save data
SaveData('/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_lopes_dp1/postprocessing/data.csv', proxy=plotOverLine1, ChooseArraysToWrite=1,
    PointDataArrays=['arc_length', 'f'])
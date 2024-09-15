# trace generated using paraview version 5.13.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3 Reader S'
txdmf = Xdmf3ReaderS(registrationName='T.xdmf', FileName=['/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_soni_dp1_fem/fenicsx/results/T.xdmf'])

UpdatePipeline(time=0.0, proxy=txdmf)

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(registrationName='PlotOverLine1', Input=txdmf)

# Properties modified on plotOverLine1
plotOverLine1.Point1 = [0.0, 0.009999999776482582, 0.0]
plotOverLine1.Point2 = [0.019999999552965164, 0.009999999776482582, 0.0]

UpdatePipeline(time=150.0, proxy=plotOverLine1)

# set active source
SetActiveSource(txdmf)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=plotOverLine1)

# create a new 'Plot Over Line'
plotOverLine2 = PlotOverLine(registrationName='PlotOverLine2', Input=txdmf)

# set active source
SetActiveSource(plotOverLine1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=plotOverLine2)

# set active source
SetActiveSource(plotOverLine2)

# set active source
SetActiveSource(plotOverLine1)

# set active source
SetActiveSource(plotOverLine2)

# Properties modified on plotOverLine2
plotOverLine2.Point1 = [0.0, 0.0075, 0.0]
plotOverLine2.Point2 = [0.019999999552965164, 0.0075, 0.0]

UpdatePipeline(time=150.0, proxy=plotOverLine2)

# set active source
SetActiveSource(txdmf)

# create a new 'Plot Over Line'
plotOverLine3 = PlotOverLine(registrationName='PlotOverLine3', Input=txdmf)

# Properties modified on plotOverLine3
plotOverLine3.Point1 = [0.0, 0.005, 0.0]
plotOverLine3.Point2 = [0.019999999552965164, 0.005, 0.0]

UpdatePipeline(time=150.0, proxy=plotOverLine3)

# set active source
SetActiveSource(plotOverLine1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=plotOverLine3)

# save data
SaveData('/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_soni_dp1_fem/postprocessing/z0.csv', proxy=plotOverLine1, ChooseArraysToWrite=1,
    PointDataArrays=['arc_length', 'f'])

# set active source
SetActiveSource(plotOverLine2)

# save data
SaveData('/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_soni_dp1_fem/postprocessing/z25.csv', proxy=plotOverLine2, ChooseArraysToWrite=1,
    PointDataArrays=['arc_length', 'f'])

# set active source
SetActiveSource(plotOverLine3)

# save data
SaveData('/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_soni_dp1_fem/postprocessing/z5.csv', proxy=plotOverLine3, ChooseArraysToWrite=1,
    PointDataArrays=['arc_length', 'f'])
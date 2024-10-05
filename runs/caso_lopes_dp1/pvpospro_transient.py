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

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
txdmfDisplay = Show(txdmf, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
txdmfDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.014999999664723873, 0.019999999552965164, 0.13399999700486662]
renderView1.CameraFocalPoint = [0.014999999664723873, 0.019999999552965164, 0.0]

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
txdmfDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'f'
fLUT = GetColorTransferFunction('f')

# get opacity transfer function/opacity map for 'f'
fPWF = GetOpacityTransferFunction('f')

# get 2D transfer function for 'f'
fTF2D = GetTransferFunction2D('f')

# create a query selection
QuerySelect(QueryString='(pointIsNear([(0, 0.036, 0),], 1e-6, inputs))', FieldType='POINT', InsideOut=0)

# create a new 'Extract Selection'
extractSelection1 = ExtractSelection(registrationName='ExtractSelection1', Input=txdmf)

# show data in view
extractSelection1Display = Show(extractSelection1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
extractSelection1Display.Representation = 'Surface'

# hide data in view
Hide(txdmf, renderView1)

# show color bar/color legend
extractSelection1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=extractSelection1)

# Create a new 'Quartile Chart View'
quartileChartView1 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime1Display = Show(plotDataOverTime1, quartileChartView1, 'QuartileChartRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView1, layout=layout1, hint=0)

# Properties modified on plotDataOverTime1Display
plotDataOverTime1Display.SeriesOpacity = ['f (stats)', '1', 'vtkOriginalPointIds (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'f (stats)', '0', 'vtkOriginalPointIds (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'f (stats)', '1', 'vtkOriginalPointIds (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'f (stats)', '2', 'vtkOriginalPointIds (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime1Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'f (stats)', '0', 'vtkOriginalPointIds (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'f (stats)', '4', 'vtkOriginalPointIds (stats)', '4', 'vtkValidPointMask (stats)', '4']

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
quartileChartView1.Update()

# save data
SaveData('/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_lopes_dp1/postprocessing/data.csv', proxy=plotDataOverTime1, ChooseArraysToWrite=1,
    RowDataArrays=['Time', 'avg(f)'],
    FieldAssociation='Row Data')

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(185, 756)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.014999999664723873, 0.019999999552965164, 0.13399999700486662]
renderView1.CameraFocalPoint = [0.014999999664723873, 0.019999999552965164, 0.0]
renderView1.CameraParallelScale = 0.09742267823480454


##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
# RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
# Interact()
#
## Save a screenshot of the active view
# SaveScreenshot("path/to/screenshot.png")
#
## Save a screenshot of a layout (multiple splitted view)
# SaveScreenshot("path/to/screenshot.png", GetLayout())
#
## Save all "Extractors" from the pipeline browser
# SaveExtracts()
#
## Save a animation of the current active view
# SaveAnimation()
#
## Please refer to the documentation of paraview.simple
## https://www.paraview.org/paraview-docs/latest/python/paraview.simple.html
##--------------------------------------------
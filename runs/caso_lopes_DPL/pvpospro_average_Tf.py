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

# create a new 'Extract Cells By Region'
extractCellsByRegion1 = ExtractCellsByRegion(registrationName='ExtractCellsByRegion1', Input=txdmf)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=extractCellsByRegion1.IntersectWith)

# Properties modified on extractCellsByRegion1
extractCellsByRegion1.IntersectWith = 'Box'
extractCellsByRegion1.Extractintersected = 1

# Properties modified on extractCellsByRegion1.IntersectWith
extractCellsByRegion1.IntersectWith.Position = [0.0, 0.031, -1e-05]
extractCellsByRegion1.IntersectWith.Length = [0.00775, 0.005, 1e-05]

# show data in view
extractCellsByRegion1Display = Show(extractCellsByRegion1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
extractCellsByRegion1Display.Representation = 'Surface'

# hide data in view
Hide(txdmf, renderView1)

# show color bar/color legend
extractCellsByRegion1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(txdmf)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=extractCellsByRegion1.IntersectWith)

# Properties modified on animationScene1
animationScene1.AnimationTime = 710.0

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# rescale color and/or opacity maps used to exactly fit the current data range
txdmfDisplay.RescaleTransferFunctionToDataRange(False, True)

# set active source
SetActiveSource(extractCellsByRegion1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=extractCellsByRegion1.IntersectWith)

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=extractCellsByRegion1)

# Properties modified on calculator1
calculator1.ResultArrayName = 'r'
calculator1.Function = 'coordsX'

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'

# hide data in view
Hide(extractCellsByRegion1, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'r'
rLUT = GetColorTransferFunction('r')

# get opacity transfer function/opacity map for 'r'
rPWF = GetOpacityTransferFunction('r')

# get 2D transfer function for 'r'
rTF2D = GetTransferFunction2D('r')

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=calculator1)

# Properties modified on calculator2
calculator2.ResultArrayName = 'integrant'
calculator2.Function = 'f*r'

# show data in view
calculator2Display = Show(calculator2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator2Display.Representation = 'Surface'

# hide data in view
Hide(calculator1, renderView1)

# show color bar/color legend
calculator2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'integrant'
integrantLUT = GetColorTransferFunction('integrant')

# get opacity transfer function/opacity map for 'integrant'
integrantPWF = GetOpacityTransferFunction('integrant')

# get 2D transfer function for 'integrant'
integrantTF2D = GetTransferFunction2D('integrant')

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=calculator2)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Calculator'
calculator3 = Calculator(registrationName='Calculator3', Input=integrateVariables1)

# Properties modified on calculator3
calculator3.ResultArrayName = 'average_gnp'
calculator3.Function = 'integrant/r'

# show data in view
calculator3Display = Show(calculator3, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(integrateVariables1, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# set active source
SetActiveSource(txdmf)

# create a new 'Extract Cells By Region'
extractCellsByRegion2 = ExtractCellsByRegion(registrationName='ExtractCellsByRegion2', Input=txdmf)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=extractCellsByRegion2.IntersectWith)

# hide data in view
Hide(calculator3, spreadSheetView1)

# set active view
SetActiveView(renderView1)

# hide data in view
Hide(calculator2, renderView1)

# set active source
SetActiveSource(txdmf)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=extractCellsByRegion2.IntersectWith)

# show data in view
txdmfDisplay = Show(txdmf, renderView1, 'UnstructuredGridRepresentation')

# show color bar/color legend
txdmfDisplay.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# set active source
SetActiveSource(extractCellsByRegion2)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=extractCellsByRegion2.IntersectWith)

# Properties modified on extractCellsByRegion2
extractCellsByRegion2.IntersectWith = 'Box'
extractCellsByRegion2.ExtractionSide = 'outside'

# Properties modified on extractCellsByRegion2.IntersectWith
extractCellsByRegion2.IntersectWith.Position = [0.0, 0.031, -1.0000000000032756e-05]
extractCellsByRegion2.IntersectWith.Length = [0.00775, 0.005, 1e-05]

# show data in view
extractCellsByRegion2Display = Show(extractCellsByRegion2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
extractCellsByRegion2Display.Representation = 'Surface'

# hide data in view
Hide(txdmf, renderView1)

# show color bar/color legend
extractCellsByRegion2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# hide data in view
Hide(extractCellsByRegion2, renderView1)

# set active source
SetActiveSource(extractCellsByRegion2)

# show data in view
extractCellsByRegion2Display = Show(extractCellsByRegion2, renderView1, 'UnstructuredGridRepresentation')

# show color bar/color legend
extractCellsByRegion2Display.SetScalarBarVisibility(renderView1, True)

#changing interaction mode based on data extents
renderView1.CameraPosition = [0.014999999664723873, 0.019999999552965164, 0.13399999700486662]

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# Properties modified on extractCellsByRegion2
extractCellsByRegion2.Extractintersected = 1

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractCellsByRegion2
extractCellsByRegion2.Extractintersected = 0

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractCellsByRegion2
extractCellsByRegion2.ExtractionSide = 'inside'

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractCellsByRegion2
extractCellsByRegion2.ExtractionSide = 'outside'

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractCellsByRegion2.IntersectWith
extractCellsByRegion2.IntersectWith.Position = [0.0, 0.031, -0.001]
extractCellsByRegion2.IntersectWith.Length = [0.00775, 0.005, 0.001]

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Calculator'
calculator4 = Calculator(registrationName='Calculator4', Input=extractCellsByRegion2)

# Properties modified on calculator4
calculator4.ResultArrayName = 'r'
calculator4.Function = 'coordsX'

# show data in view
calculator4Display = Show(calculator4, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator4Display.Representation = 'Surface'

# hide data in view
Hide(extractCellsByRegion2, renderView1)

# show color bar/color legend
calculator4Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Calculator'
calculator5 = Calculator(registrationName='Calculator5', Input=calculator4)

# Properties modified on calculator5
calculator5.Function = 'f*r'

# show data in view
calculator5Display = Show(calculator5, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator5Display.Representation = 'Surface'

# hide data in view
Hide(calculator4, renderView1)

# show color bar/color legend
calculator5Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

# create a new 'Integrate Variables'
integrateVariables2 = IntegrateVariables(registrationName='IntegrateVariables2', Input=calculator5)

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.BlockSize = 1024

# show data in view
integrateVariables2Display = Show(integrateVariables2, spreadSheetView2, 'SpreadSheetRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView2, layout=layout1, hint=1)

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
spreadSheetView2.Update()

# create a new 'Calculator'
calculator6 = Calculator(registrationName='Calculator6', Input=integrateVariables2)

# set active source
SetActiveSource(calculator5)

# Properties modified on calculator6
calculator6.Function = ''

# show data in view
calculator6Display = Show(calculator6, spreadSheetView2, 'SpreadSheetRepresentation')

# hide data in view
Hide(integrateVariables2, spreadSheetView2)

# Properties modified on calculator5
calculator5.ResultArrayName = 'integrant'

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
spreadSheetView2.Update()

# set active source
SetActiveSource(integrateVariables2)

# set active source
SetActiveSource(calculator6)

# Properties modified on calculator6
calculator6.ResultArrayName = 'average_agar'
calculator6.Function = 'integrant/r'

# update the view to ensure updated data information
spreadSheetView2.Update()

# set active source
SetActiveSource(calculator3)

# set active source
SetActiveSource(calculator6)

# create a new 'Append Attributes'
appendAttributes1 = AppendAttributes(registrationName='AppendAttributes1', Input=[calculator3, calculator6])

# show data in view
appendAttributes1Display = Show(appendAttributes1, spreadSheetView2, 'SpreadSheetRepresentation')

# hide data in view
Hide(calculator6, spreadSheetView2)

# update the view to ensure updated data information
spreadSheetView2.Update()

# save data
SaveData('/home/rc/Projects/fototermal/github/fem_photothermal_cell_death/runs/caso_lopes_dp1/postprocessing/data.csv', proxy=appendAttributes1, ChooseArraysToWrite=1,
    PointDataArrays=['average_agar', 'average_gnp'],
    AddMetaData=0)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(897, 761)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.014999999664723873, 0.019999999552965164, 0.1443849400320622]
renderView1.CameraFocalPoint = [0.014999999664723873, 0.019999999552965164, -5.000000000016378e-06]
renderView1.CameraParallelScale = 0.03810483862006469


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
import vtk
import math
### ANU SAMPLE FOLDERS ####
### ANU 10 - Lot10_Yshape_CF8_2AR125.5
### ANU 11 - Stone1_TwoAR1265_3.4MM_CF8_10um
### ANU 12 - Stone2_Triangularprism_CF8_2AR126.5
### ANU 13 - Stone3_Concavesurf_CF8_TwoAR126
### ANU 14 - Stone4_CF8_2AR126_ReM2Rep1
### ANU 15 - Stone5_Cuboidroughsurf2_CF8_2AR126
### ANU 16 - Stone6_Starshape_CF8_TwoAR126
### ANU 17 - Stone7_Pyramid_CF8_2AR125.5
### ANU 18 - Stone7_Pyramid_CF8_2AR125.5
### ANU 19 - Stone9_Smalltriangle_CF8_2AR125.5

path10 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU10-AT074/Lot10_Yshape_CF8_2AR125.5/"
path11 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU11-AR112/Stone1_TwoAR1265_3.4MM_CF8_10um/"
path12 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU12-AP160RW/Stone2_Triangularprism_CF8_2AR126.5/"
path13 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU13-AP145RW/Stone3_Concavesurf_CF8_TwoAR126/"
path14 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU14-AR371/Stone4_CF8_2AR126_ReM2Rep1/"
path15 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU15-AR392/Stone5_Cuboidroughsurf2_CF8_2AR126/"
path16 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU16-PG0340/Stone6_Starshape_CF8_TwoAR126/"
path17 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU17-PG0349/Stone7_Pyramid_CF8_2AR125.5/"
path18 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU18-PG0155/Stone8_ReM1_DeepFcs_TwoAR1255_CF8/"
path19 = "C:/Users/abdullah/Desktop/VTK/Python files/DiamondSample/ANU19-AT021/Stone9_Smalltriangle_CF8_2AR125.5/"

from vtk.util.colors import tomato

fileName = "vol_t00_x5_70_d4pt5_inner.vti"

colors = vtk.vtkNamedColors()

# This is a simple volume rendering example that
# uses a vtkFixedPointVolumeRayCastMapper

# Create the standard renderer, render window
# and interactor.
ren1 = vtk.vtkRenderer()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Create the reader for the data.
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(path14+ fileName)

# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtk.vtkPiecewiseFunction()
#opacityTransferFunction.AddPoint(20, 0.0)
#opacityTransferFunction.AddPoint(255, 0.2)
opacityTransferFunction.AddPoint(2440.0, 0.0)
opacityTransferFunction.AddPoint( 2800.0,0.97)

# Create transSfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
#volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
#volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

vExtractor = vtk.vtkMarchingCubes()
vExtractor.SetInputConnection(reader.GetOutputPort())
vExtractor.SetValue(0,2550)
#print(vExtractor.GetNumberOfContours())
#print(vExtractor.GetValues())


vNormals = vtk.vtkPolyDataNormals()
vNormals.SetInputConnection(vExtractor.GetOutputPort())
vNormals.SplittingOn()
vNormals.ConsistencyOn()
vNormals.AutoOrientNormalsOn()
vNormals.SetFeatureAngle(180.0)

vStripper = vtk.vtkStripper()
vStripper.SetInputConnection(vNormals.GetOutputPort())

vLocator = vtk.vtkCellLocator()
vLocator.SetDataSet(vExtractor.GetOutput())
vLocator.LazyEvaluationOn()
#print(vLocator.GetDataSet())

vMapper = vtk.vtkPolyDataMapper()
vMapper.SetInputConnection(vStripper.GetOutputPort())
vMapper.ScalarVisibilityOff()

vProperty = vtk.vtkProperty()
vProperty.SetColor(1.0,1.0,0.9)

v = vtk.vtkActor()
v.SetMapper(vMapper)
v.SetProperty(vProperty)

# the picker
picker = vtk.vtkVolumePicker()
picker.SetTolerance(1e-6)
picker.SetVolumeOpacityIsovalue(0.075)
# locator is optional, but improves performance for large polydata
picker.AddLocator(vLocator)

glyphSphere = vtk.vtkSphereSource()
glyphSphere.SetRadius(0.009)

glyph2 = vtk.vtkGlyph3D()
glyph2.SetInputConnection(vExtractor.GetOutputPort())
glyph2.SetSourceConnection(glyphSphere.GetOutputPort())
glyph2.SetScaleModeToDataScalingOff()
glyph2.SetIndexModeToScalar()
glyph2.GeneratePointIdsOn()
glyph2.FillCellDataOn()
glyph2.GetOutputPointsPrecision()
#print(glyph2.GetPointIdsName())
#print(glyph2.GetOutputDataObject)

glyphMapper2 = vtk.vtkPolyDataMapper()
glyphMapper2.SetInputConnection(glyph2.GetOutputPort())
glyphMapper2.ScalarVisibilityOff()
glyphMapper2.Update()
glyphActor2 = vtk.vtkActor()
glyphActor2.SetMapper(glyphMapper2)
glyphActor2.AddPosition(7.5, 0, 0)
glyphActor2.GetProperty().SetColor(1,1,0.9)
glyphActor2.GetProperty().SetDiffuseColor(tomato)
glyphActor2

#print(glyph2.GetExecutive().GetOutputData(0))
#dir(glyph2.GetExecutive().GetOutputData(0))
points = vtk.vtkPoints()

numPoints = glyph2.GetExecutive().GetOutputData(0).GetNumberOfPoints()
outputData = glyph2.GetExecutive().GetOutputData(0)
'''
for i in range (0, numPoints-1):
    points.InsertNextPoint(outputData.GetPoint(i))
'''
pointsPolydata = vtk.vtkPolyData()
pointsPolydata.SetPoints(points)

# Points inside test
selectEnclosedPoints = vtk.vtkSelectEnclosedPoints()
selectEnclosedPoints.SetInputData(pointsPolydata)
selectEnclosedPoints.SetSurfaceData(glyph2.GetOutput())
selectEnclosedPoints.Update()
'''
for i in range(0,98):
    print ( "point" + str(i) + ':' + str(selectEnclosedPoints.IsInside(i)))
    
bb = selectEnclosedPoints.GetOutput().GetPointData().GetArray("InputPointIds")


insideArray = vtk.vtkUnsignedCharArray().SafeDownCast(bb)

#for i in range ( 0, insideArray.GetNumberOfTuples()):
#    print( str(i) + ':' +  str(insideArray.GetComponent(i,0)))
vertexGlyphFilter = vtk.vtkVertexGlyphFilter()
vertexGlyphFilter.AddInputData(pointsPolydata)
vertexGlyphFilter.Update()

pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(vertexGlyphFilter.GetOutputPort())

pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)
pointsActor.GetProperty().SetPointSize(5)
pointsActor.GetProperty().SetColor(0,0,1)
'''
ren1.AddVolume(volume)
#ren1.AddActor(pointsActor)
ren1.AddViewProp(v)
ren1.AddViewProp(glyphActor2)

#ren1.SetBacground(colors.GetColor3d("Wheat"))
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()

renWin.SetSize(600, 600)
renWin.Render()

iren.Start()



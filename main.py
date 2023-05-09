
import vtk
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkCutter, vtkTubeFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkProperty,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource
)

colors = vtkNamedColors()


def create_skin_tubes(skinFilter, numberOfCuts):
    skinFilter.Update()
    bounds = skinFilter.GetOutput().GetBounds()
    plane = vtkPlane()
    plane.SetOrigin((bounds[1] + bounds[0]) / 2.0,
                    (bounds[3] + bounds[2]) / 2.0, bounds[4])
    plane.SetNormal(0, 0, 1)

    # Create cutter
    high = plane.EvaluateFunction(
        (bounds[1] + bounds[0]) / 2.0, (bounds[3] + bounds[2]) / 2.0, bounds[5])

    cutter = vtkCutter()
    cutter.SetInputConnection(skinFilter.GetOutputPort())  # Change this line
    cutter.SetCutFunction(plane)
    cutter.GenerateValues(numberOfCuts, 0.99, 0.99 * high)

    # Add vtkTubeFilter to create tubes
    tubeFilter = vtkTubeFilter()
    tubeFilter.SetInputConnection(cutter.GetOutputPort())
    tubeFilter.SetRadius(0.5)  # Set the radius of the tubes
    tubeFilter.SetNumberOfSides(12)
    tubeFilter.CappingOn()

    cutterMapper = vtkPolyDataMapper()
    cutterMapper.SetInputConnection(tubeFilter.GetOutputPort())
    cutterMapper.ScalarVisibilityOff()

    cutterActor = vtkActor()
    cutterActor.GetProperty().SetColor(vtkNamedColors().GetColor3d('Banana'))
    cutterActor.SetMapper(cutterMapper)
    return cutterActor


def get_sources_functions():
    return [
        source1,
        source2,
        source3,
        source4
    ]


def source1(skinMapper, bonesMapper, skinFilter, bonesFilter):
    # Create a mapper and actor
    skinActor = vtkActor()
    skinActor.SetMapper(skinMapper)
    skinActor.GetProperty().SetDiffuse(0.8)
    skinActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Pink'))
    skinActor.GetProperty().SetSpecular(0.8)
    skinActor.GetProperty().SetSpecularPower(120.0)
    skinActor.GetProperty().SetOpacity(1.0)

    backFaceProp = vtkProperty()
    backFaceProp.SetDiffuseColor(colors.GetColor3d('Tomato'))
    backFaceProp.SetSpecular(0.8)
    backFaceProp.SetSpecularPower(120.0)
    backFaceProp.SetOpacity(1.0)
    skinActor.SetBackfaceProperty(backFaceProp)

    bonesActor = vtkActor()
    bonesActor.SetMapper(bonesMapper)
    bonesActor.GetProperty().SetDiffuse(0.8)
    bonesActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    bonesActor.GetProperty().SetSpecular(0.8)
    bonesActor.GetProperty().SetSpecularPower(120.0)

    clipTransf = vtk.vtkTransform()
    clipTransf.Translate(-50, 0, -120)

    sphere = vtk.vtkSphere()
    sphere.SetRadius(65)
    sphere.SetTransform(clipTransf)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skinFilter.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0)
    skinMapper.SetInputConnection(clipper.GetOutputPort())

    return skinActor, bonesActor


def source2(skinMapper, bonesMapper, skinFilter, bonesFilter):
    # Create a mapper and actor
    skinActor = vtkActor()
    skinActor.SetMapper(skinMapper)
    skinActor.GetProperty().SetDiffuse(0.8)
    skinActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Pink'))
    skinActor.GetProperty().SetSpecular(0.8)
    skinActor.GetProperty().SetSpecularPower(120.0)
    skinActor.GetProperty().SetOpacity(0.5)

    backFaceProp = vtkProperty()
    backFaceProp.SetDiffuseColor(colors.GetColor3d('Tomato'))
    backFaceProp.SetSpecular(0.8)
    backFaceProp.SetSpecularPower(120.0)
    backFaceProp.SetOpacity(1.0)
    skinActor.SetBackfaceProperty(backFaceProp)

    bonesActor = vtkActor()
    bonesActor.SetMapper(bonesMapper)
    bonesActor.GetProperty().SetDiffuse(0.8)
    bonesActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    bonesActor.GetProperty().SetSpecular(0.8)
    bonesActor.GetProperty().SetSpecularPower(120.0)

    clipTransf = vtk.vtkTransform()
    clipTransf.Translate(-50, 0, -120)

    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetTransform(clipTransf)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skinFilter.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0)
    skinMapper.SetInputConnection(clipper.GetOutputPort())

    return skinActor, bonesActor


def source3(skinMapper, bonesMapper, skinFilter, bonesFilter):
    bonesActor = vtkActor()
    bonesActor.SetMapper(bonesMapper)
    bonesActor.GetProperty().SetDiffuse(0.8)
    bonesActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Pink'))
    bonesActor.GetProperty().SetSpecular(0.8)
    bonesActor.GetProperty().SetSpecularPower(120.0)

    clipTransf = vtk.vtkTransform()
    clipTransf.Translate(-50, 0, -120)

    sphere = vtk.vtkSphere()
    sphere.SetRadius(75)
    sphere.SetTransform(clipTransf)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skinFilter.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0)
    skinMapper.SetInputConnection(clipper.GetOutputPort())

    tubeActor = create_skin_tubes(skinFilter, 20)

    return bonesActor, tubeActor


def source4(skinMapper, bonesMapper, skinFilter, bonesFilter):
    skinActor = vtkActor()
    skinActor.SetMapper(skinMapper)
    skinActor.GetProperty().SetDiffuse(0.8)
    skinActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Green'))
    skinActor.GetProperty().SetSpecular(0.8)
    skinActor.GetProperty().SetSpecularPower(120.0)
    skinActor.GetProperty().SetOpacity(0.5)

    backFaceProp = vtkProperty()
    backFaceProp.SetDiffuseColor(colors.GetColor3d('Tomato'))
    backFaceProp.SetSpecular(0.8)
    backFaceProp.SetSpecularPower(120.0)
    backFaceProp.SetOpacity(1.0)
    skinActor.SetBackfaceProperty(backFaceProp)

    bonesActor = vtkActor()
    bonesActor.SetMapper(bonesMapper)
    bonesActor.GetProperty().SetDiffuse(0.8)
    bonesActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    bonesActor.GetProperty().SetSpecular(0.8)
    bonesActor.GetProperty().SetSpecularPower(120.0)

    clipTransf = vtk.vtkTransform()
    clipTransf.Translate(-50, 0, -120)

    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetTransform(clipTransf)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skinFilter.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0)
    skinMapper.SetInputConnection(clipper.GetOutputPort())

    return skinActor, bonesActor


def main():
    InputFilename = "vw_knee.slc"

    # vtkSLCReader to read.
    reader = vtkSLCReader()
    reader.SetFileName(InputFilename)
    reader.Update()

    render_window = vtkRenderWindow()
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(render_window)

    # Define viewport ranges.
    xmins = [0, 0.5, 0, 0.5]
    xmaxs = [0.5, 1, 0.5, 1]
    ymins = [0, 0, 0.5, 0.5]
    ymaxs = [0.5, 0.5, 1, 1]

    # Have some fun with colors.
    backgrounds = ['AliceBlue', 'GhostWhite', 'WhiteSmoke', 'Seashell']

    sources = get_sources_functions()

    for i in range(len(sources)):
        ren = vtkRenderer()
        render_window.AddRenderer(ren)
        ren.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])

        # Share the camera between viewports.
        if i == 0:
            camera = ren.GetActiveCamera()
            camera.Azimuth(30)
            camera.Elevation(30)
        else:
            ren.SetActiveCamera(camera)

        wrapper = vtk.vtkCubeSource()
        wrapper.SetXLength(1000.0)
        wrapper.SetYLength(1500)
        wrapper.SetZLength(2000)

        wrapperMapper = vtk.vtkPolyDataMapper()
        wrapperMapper.SetInputConnection(wrapper.GetOutputPort())

        wrapperActor = vtk.vtkActor()
        wrapperActor.SetMapper(wrapperMapper)

        # Couleur du parallélépipède (gris clair)
        wrapperActor.GetProperty().SetColor(0.7, 0.7, 0.7)
        # Transparence (0.0 = totalement transparent, 1.0 = totalement opaque)
        wrapperActor.GetProperty().SetOpacity(0)
        # Activation de la visibilité des arêtes
        wrapperActor.GetProperty().EdgeVisibilityOn()
        wrapperActor.GetProperty().SetEdgeColor(
            0.0, 0.0, 0.0)  # Couleur des arêtes (noir)

        skinFilter = vtkContourFilter()
        skinFilter.SetInputConnection(reader.GetOutputPort())
        skinFilter.SetValue(0, 50)

        bonesFilter = vtkContourFilter()
        bonesFilter.SetInputConnection(reader.GetOutputPort())
        bonesFilter.SetValue(50, 72)

        skinMapper = vtkPolyDataMapper()
        skinMapper.SetInputConnection(skinFilter.GetOutputPort())
        skinMapper.SetScalarVisibility(0)

        bonesMapper = vtkPolyDataMapper()
        bonesMapper.SetInputConnection(bonesFilter.GetOutputPort())
        bonesMapper.SetScalarVisibility(0)

        actors = sources[i](skinMapper, bonesMapper, skinFilter, bonesFilter)

        #ren.AddActor(wrapperActor)

        for actor in actors:
            ren.AddActor(actor)

        cam1 = ren.GetActiveCamera()
        cam1.SetFocalPoint(0.0, 0.0, 0.0)
        cam1.SetPosition(0.0, -1.0, 0.0)
        cam1.SetViewUp(0.0, 0.0, -1.0)
        cam1.Azimuth(-90.0)
        ren.ResetCamera()
        ren.ResetCameraClippingRange()

        ren.SetBackground(colors.GetColor3d(backgrounds[i]))
        ren.ResetCamera()

    render_window.Render()
    render_window.SetWindowName('MultipleViewPorts')
    render_window.SetSize(1200, 1200)
    # render_window.SetWindowFocus(True)

    screen_size = render_window.GetScreenSize()
    window_size = render_window.GetSize()
    render_window.SetPosition(
        int((screen_size[0] - window_size[0]) / 2),
        int((screen_size[1] - window_size[1]) / 2)
    )

    iren.SetInteractorStyle(
        vtkmodules.vtkInteractionStyle.vtkInteractorStyleTrackballCamera()
    )
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    main()

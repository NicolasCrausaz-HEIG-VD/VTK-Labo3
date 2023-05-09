
import vtk
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkSLCReader
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


def main():
    InputFilename = "vw_knee.slc"

    # vtkSLCReader to read.
    reader = vtkSLCReader()
    reader.SetFileName(InputFilename)
    reader.Update()

    colors = vtkNamedColors()
    rw = vtkRenderWindow()
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(rw)

    # Define viewport ranges.
    xmins = [0, .5, 0, .5]
    xmaxs = [0.5, 1, 0.5, 1]
    ymins = [0, 0, .5, .5]
    ymaxs = [0.5, 0.5, 1, 1]

    # Have some fun with colors.
    ren_bkg = ['AliceBlue', 'GhostWhite', 'WhiteSmoke', 'Seashell']
    actor_color = ['Bisque', 'RosyBrown', 'Goldenrod', 'Chocolate']

    # sources = get_sources()

    for i in range(4):
        ren = vtkRenderer()
        rw.AddRenderer(ren)
        ren.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])

        # Share the camera between viewports.
        if i == 0:
            camera = ren.GetActiveCamera()
            camera.Azimuth(30)
            camera.Elevation(30)
        else:
            ren.SetActiveCamera(camera)

        # Create a mapper and actor
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
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

        actor = vtkActor()
        actor.GetProperty().SetColor(colors.GetColor3d(actor_color[i]))
        actor.SetMapper(mapper)
        ren.AddActor(skinActor)
        ren.AddActor(bonesActor)

        cam1 = ren.GetActiveCamera()
        cam1.SetFocalPoint(0.0, 0.0, 0.0)
        cam1.SetPosition(0.0, -1.0, 0.0)
        cam1.SetViewUp(0.0, 0.0, -1.0)
        cam1.Azimuth(-90.0)
        ren.ResetCamera()
        ren.ResetCameraClippingRange()

        ren.SetBackground(colors.GetColor3d(ren_bkg[i]))

        ren.ResetCamera()
        rw.Render()
        rw.SetWindowName('MultipleViewPorts')
        rw.SetSize(1200, 1200)

        screen_size = rw.GetScreenSize()
        window_size = rw.GetSize()
        rw.SetPosition(
            int((screen_size[0] - window_size[0]) / 2),
            int((screen_size[1] - window_size[1]) / 2)
        )

    rw.Render()
    iren.SetInteractorStyle(
        vtkmodules.vtkInteractionStyle.vtkInteractorStyleTrackballCamera()
    )
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    main()

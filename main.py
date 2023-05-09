
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


def main():
    InputFilename = "vw_knee.slc"

    colors = vtkNamedColors()

    # vtkSLCReader to read.
    reader = vtkSLCReader()
    reader.SetFileName(InputFilename)
    reader.Update()

    # Create a mapper.
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    skinFilter = vtkContourFilter()
    skinFilter.SetInputConnection(reader.GetOutputPort())
    skinFilter.SetValue(0, 50)

    bonesFilter = vtkContourFilter()
    bonesFilter.SetInputConnection(reader.GetOutputPort())
    bonesFilter.SetValue(50, 72)

    outliner = vtkOutlineFilter()
    outliner.SetInputConnection(reader.GetOutputPort())
    outliner.Update()

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
    skinActor.GetProperty().BackfaceCullingOn()


    bonesActor = vtkActor()
    bonesActor.SetMapper(bonesMapper)
    bonesActor.GetProperty().SetDiffuse(0.8)
    bonesActor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    bonesActor.GetProperty().SetSpecular(0.8)
    bonesActor.GetProperty().SetSpecularPower(120.0)

    # Create a rendering window and renderer.
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(500, 500)

    # Create a renderwindowinteractor.
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Assign actor to the renderer.
    renderer.AddActor(bonesActor)
    renderer.AddActor(skinActor)
    renderer.SetBackground(colors.GetColor3d('SlateGray'))

    # Pick a good view
    cam1 = renderer.GetActiveCamera()
    cam1.SetFocalPoint(0.0, 0.0, 0.0)
    cam1.SetPosition(0.0, -1.0, 0.0)
    cam1.SetViewUp(0.0, 0.0, -1.0)
    cam1.Azimuth(-90.0)
    renderer.ResetCamera()
    renderer.ResetCameraClippingRange()

    renderWindow.SetWindowName('ReadSLC')
    renderWindow.SetSize(640, 512)
    renderWindow.Render()

    # Use trackball interaction style for easy mouse controll
    
    

    # Enable user interface interactor.
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()

    # interactor = vtkRenderWindowInteractor()
    # interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    # interactor.SetRenderWindow(renderWindowInteractor)
    # renderWindowInteractor.Render()
    # interactor.Initialize()
    # interactor.Start()


if __name__ == '__main__':
    main()
import os
import vtk
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkCutter, vtkTubeFilter, vtkStripper, vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkDistancePolyDataFilter
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

colors = vtkNamedColors()
colors.SetColor('Skin', [240, 184, 160, 255])


def create_skin_tubes(skin_filter, spacing):
    skin_filter.Update()
    bounds = skin_filter.GetOutput().GetBounds()
    height = (bounds[5] - bounds[4])
    number_of_cuts = int(height / spacing)
    # Create a plane at the desired height
    plane = vtkPlane()
    plane.SetOrigin((bounds[1] + bounds[0]) / 2.0,
                    (bounds[3] + bounds[2]) / 2.0, bounds[4])
    plane.SetNormal(0, 0, 1)

    # Create cutter
    cutter = vtkCutter()
    cutter.SetInputConnection(skin_filter.GetOutputPort())
    cutter.SetCutFunction(plane)
    # Generate the cut at a specific height
    cutter.GenerateValues(number_of_cuts, 0, height)

    # Apply vtkStripper to generate polylines from the cutter
    stripper = vtkStripper()
    stripper.SetInputConnection(cutter.GetOutputPort())
    stripper.Update()

    # Add vtkTubeFilter to create tubes
    tube_filter = vtkTubeFilter()
    tube_filter.SetInputConnection(stripper.GetOutputPort())
    tube_filter.SetRadius(1.0)
    tube_filter.SetNumberOfSides(10)
    tube_filter.CappingOn()

    # Create mapper and actor for the tubes
    cutter_mapper = vtkPolyDataMapper()
    cutter_mapper.SetInputConnection(tube_filter.GetOutputPort())
    cutter_mapper.ScalarVisibilityOff()

    cutter_actor = vtkActor()
    cutter_actor.GetProperty().SetColor(colors.GetColor3d('Skin'))
    cutter_actor.SetMapper(cutter_mapper)

    return cutter_actor


def get_sources_functions(gen_skin_mapper, gen_bones_mapper, skin_filter, bones_filter):
    return [
        source1(gen_skin_mapper, gen_bones_mapper, skin_filter),
        source4(skin_filter, bones_filter),
        source3(gen_bones_mapper, skin_filter),
        source2(gen_skin_mapper, gen_bones_mapper, skin_filter),
    ]


def source1(gen_skin_mapper, gen_bones_mapper, skin_filter):
    skin_mapper = gen_skin_mapper();
    bones_mapper = gen_bones_mapper();
    # Create a mapper and actor
    skin_actor = vtkActor()
    skin_actor.SetMapper(skin_mapper)
    skin_actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Skin'))
    skin_actor.GetProperty().SetOpacity(1.0)

    back_face_prop = vtkProperty()
    back_face_prop.SetDiffuseColor(colors.GetColor3d('Tomato'))
    back_face_prop.SetSpecular(0.8)
    back_face_prop.SetSpecularPower(120.0)
    back_face_prop.SetOpacity(1.0)
    skin_actor.SetBackfaceProperty(back_face_prop)

    bones_actor = get_bones_actor(bones_mapper)

    clip_transf = vtk.vtkTransform()
    clip_transf.Translate(-70, -50, -100)

    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetTransform(clip_transf)

    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(50)
    sphere_source.SetCenter(70, 50, 100)
    sphere_source.SetPhiResolution(100)
    sphere_source.Update()

    sphere_mapper = vtk.vtkPolyDataMapper()
    sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

    sphere_actor = vtkActor()
    sphere_actor.SetMapper(sphere_mapper)
    sphere_actor.GetProperty().SetOpacity(0.5)
    sphere_actor.GetProperty().BackfaceCullingOn()

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skin_filter.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0)
    skin_mapper.SetInputConnection(clipper.GetOutputPort())

    return skin_actor, bones_actor, sphere_actor


def source2(gen_skin_mapper, gen_bones_mapper, skin_filter):
    skin_mapper = gen_skin_mapper();
    bones_mapper = gen_bones_mapper();
    # Create a mapper and actor
    skin_actor = vtkActor()
    skin_actor.SetMapper(skin_mapper)
    skin_actor.GetProperty().SetDiffuse(0.8)
    skin_actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Skin'))
    skin_actor.GetProperty().SetOpacity(0.5)

    back_face_prop = vtkProperty()
    back_face_prop.SetDiffuseColor(colors.GetColor3d('Tomato'))
    back_face_prop.SetSpecular(0.8)
    back_face_prop.SetSpecularPower(120.0)
    back_face_prop.SetOpacity(1.0)
    skin_actor.SetBackfaceProperty(back_face_prop)

    bones_actor = get_bones_actor(bones_mapper)

    clip_transf = vtk.vtkTransform()
    clip_transf.Translate(-70, -50, -100)

    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetTransform(clip_transf)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skin_filter.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0)
    skin_mapper.SetInputConnection(clipper.GetOutputPort())

    return skin_actor, bones_actor


def source3(gen_bones_mapper, skin_filter):
    bones_mapper = gen_bones_mapper();
    bones_actor = get_bones_actor(bones_mapper)
    tube_actor = create_skin_tubes(skin_filter, 10)

    return bones_actor, tube_actor


def source4(skin_filter, bones_filter):

    distance_filter = None

    if os.path.isfile("output.vtk"):
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName("output.vtk")
        reader.Update()
        distance_filter = reader
    else:
        distance_filter = vtkDistancePolyDataFilter()
        distance_filter.SetInputConnection(0, bones_filter.GetOutputPort())
        distance_filter.SetInputConnection(1, skin_filter.GetOutputPort())
        distance_filter.NegateDistanceOn()
        distance_filter.Update()
        write_filter_file(distance_filter)



    bones_mapper = vtkPolyDataMapper()
    bones_mapper.SetInputData(distance_filter.GetOutput())
    bones_mapper.SetScalarRange(distance_filter.GetOutput().GetScalarRange())

    bones_actor = vtkActor()
    bones_actor.SetMapper(bones_mapper)

    return [bones_actor]

def write_filter_file(distance_filter):
  writer = vtk.vtkPolyDataWriter()
  writer.SetFileName("output.vtk") 
  writer.SetInputData(distance_filter.GetOutput()) 
  writer.Write()


def get_bones_actor(bones_mapper):
    bones_actor = vtkActor()
    bones_actor.SetMapper(bones_mapper)
    bones_actor.GetProperty().SetDiffuse(0.8)
    bones_actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    bones_actor.GetProperty().SetSpecular(0.1)
    bones_actor.GetProperty().SetSpecularPower(40.0)
    return bones_actor


def main():
    input_filename = "vw_knee.slc"

    # vtkSLCReader to read the .slc file
    reader = vtkSLCReader()
    reader.SetFileName(input_filename)
    reader.Update()

    render_window = vtkRenderWindow()
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(render_window)

    # Define viewport ranges.
    xmins = [0, 0.5, 0, 0.5]
    xmaxs = [0.5, 1, 0.5, 1]
    ymins = [0, 0, 0.5, 0.5]
    ymaxs = [0.5, 0.5, 1, 1]

    backgrounds = ['LightBlue', 'Gray', 'Pink', 'Green']

    skin_filter = vtkContourFilter()
    skin_filter.SetInputConnection(reader.GetOutputPort())
    skin_filter.SetValue(0, 50)

    bones_filter = vtkContourFilter()
    bones_filter.SetInputConnection(reader.GetOutputPort())
    bones_filter.SetValue(50, 72)

    def gen_skin_mapper():
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(skin_filter.GetOutputPort())
        mapper.SetScalarVisibility(0)
        return mapper

    def gen_bones_mapper():
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(bones_filter.GetOutputPort())
        mapper.SetScalarVisibility(0)
        return mapper

    sources = get_sources_functions(gen_skin_mapper, gen_bones_mapper, skin_filter, bones_filter)

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

        # Create an edge cube using bounds
        edges = vtkOutlineFilter()
        edges.SetInputConnection(reader.GetOutputPort())

        edges_mapper = vtkPolyDataMapper()
        edges_mapper.SetInputConnection(edges.GetOutputPort())

        edges_actor = vtkActor()
        edges_actor.SetMapper(edges_mapper)
        edges_actor.GetProperty().SetColor(colors.GetColor3d('Black'))

        actors = sources[i]

        ren.AddActor(edges_actor)

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
    render_window.SetWindowName('VTK - Labo 3')
    render_window.SetSize(1200, 1200)

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

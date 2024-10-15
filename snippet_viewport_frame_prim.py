# Viewport/Frame a specific prim
import omni.kit.commands
from omni.kit.viewport.utility import get_active_viewport
from pxr import Sdf, Usd, UsdGeom

# Useful variables that will be passed to the FramePrimsCommand
camera_path = None
prim_to_frame = None
time = Usd.TimeCode.Default()
resolution = (1, 1)
zoom = 0.6

# Get the stage
stage = omni.usd.get_context().get_stage()

# Get the default prim to create the Camera underneath
default_prim = stage.GetDefaultPrim()

# Get the root Sdf.Path that the camera is created under
root_path = default_prim.GetPath() if default_prim else Sdf.Path.absoluteRootPath

# Construct a path to the object that is being framed
prim_to_frame = root_path.AppendChild("My_Cube")

# Create the Cube so that there is something to frame
UsdGeom.Cube.Define(stage, prim_to_frame)

active_viewport = get_active_viewport()
if active_viewport:
    # NOTE: there is a convenience method to frame the active selection in a Viewport:
    # from omni.kit.viewport.utility import frame_viewport_selection
    # frame_viewport_selection(active_viewport)

    # Pull meaningfull information from the Viewport to frame a specific prim
    time = active_viewport.time
    resolution = active_viewport.resolution
    camera_path = active_viewport.camera_path
else:
    # Create a camera that will be used to frame the prim_to_frame
    camera_path = root_path.AppendChild('New_Camera')
    UsdGeom.Camera.Define(stage, camera_path)

# Finally run the undo-able FramePrimsCommand
omni.kit.commands.execute(
    'FramePrimsCommand',
    # The path to the camera that is begin moved
    prim_to_move=camera_path,
    # The prim that is begin framed / looked at
    prims_to_frame=[prim_to_frame.pathString],
    # The Usd.TimCode that camera_path will use to set new location and orientation
    time_code=time,
    # The aspect_ratio of the image-place that is being viewed
    aspect_ratio=resolution[0]/resolution[1],
    # Additional slop to use for the framing
    zoom=zoom
)

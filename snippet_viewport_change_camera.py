# Viewport/Switch to a camera
from omni.kit.viewport.utility import get_active_viewport
from pxr import Tf, Sdf, Usd, UsdGeom


def snippet_create_camera(stage: Usd.Stage, camera_name: str, orthographic: bool = False) -> Sdf.Path:
    # Get the default prim to create the Camera underneath
    default_prim = stage.GetDefaultPrim()

    # Get the root Sdf.Path that the camera is created under
    root_path = default_prim.GetPath() if default_prim else Sdf.Path.absoluteRootPath

    valid_camera_name = Tf.MakeValidIdentifier(camera_name)
    if valid_camera_name != camera_name:
        print(f"'{camera_name}' was not a valid camera name, using '{valid_camera_name}'")

    # Construct the full path to the camera to be created
    camera_path = root_path.AppendChild(valid_camera_name)

    # Create the UsdGeom.Camera
    usd_camera = UsdGeom.Camera.Define(stage, camera_path)

    # Default camera in Usd is perspective, switch it to orthographic if requested
    if orthographic:
        usd_camera.GetProjectionAttr().Set(UsdGeom.Tokens.orthographic)

    return camera_path


def snippet_viewport_change_camera(camera_name: str, orthographic: bool = False):
    viewport = get_active_viewport()
    if not viewport:
        print("No active Viewport")
        return

    # Get the Usd.Stage this Viewport is viewing
    stage = viewport.stage
    if not stage:
        print(f"Viewport {viewport} has no stage")
        return

    # Create the camera, which return the Sdf.Path
    camera_path = snippet_create_camera(stage, camera_name, orthographic)

    # Finally set the Viewport's active camera to the one just created
    viewport.camera_path = camera_path


snippet_viewport_change_camera('Snippet_Ortho_Camera', True)

snippet_viewport_change_camera('Snippet_Camera')

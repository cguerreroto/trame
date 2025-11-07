r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/VTK/SimpleCone/ClientView.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/674f72774228bbcab5689417c1c5642230b1eab8

Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

from vtkmodules.vtkFiltersSources import vtkConeSource

from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vtk as vtk_widgets
from trame.widgets import vuetify3 as vuetify, vtk

# -----------------------------------------------------------------------------
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server(client_type="vue3")
state, ctrl = server.state, server.controller

state.trame__title = "VTK Local rendering"

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

cone_generator = vtkConeSource()

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_generator.SetResolution(resolution)
    ctrl.mesh_update()


def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("Cone Application")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            dense=True,
            style="max-width: 300px",
        )
        vuetify.VDivider(vertical=True, classes="mx-2")

        with vuetify.VBtn(icon=True, click=update_reset_resolution):
            vuetify.VIcon("mdi-undo-variant")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk_widgets.VtkView() as view:
                ctrl.view_reset_camera = view.reset_camera
                with vtk_widgets.VtkGeometryRepresentation():
                    html_polydata = vtk_widgets.VtkPolyData(
                        "cone", dataset=cone_generator
                    )
                    ctrl.mesh_update = html_polydata.update


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # option 1: start on default port 8080
    # server.start()

    # option 2: find a free port starting at 8080
    import socket
    
    def is_port_free(port):
        """Check if a port is free by attempting to bind to it"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            try:
                test_socket.bind(('127.0.0.1', port))
                return True
            except OSError:
                return False
    
    def find_free_port(start_port=8080, max_attempts=10):
        """Find a free port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            if is_port_free(port):
                return port
        return 0  # let OS pick if all attempts fail
    
    # determine which port to use
    default_port = 8080
    if is_port_free(default_port):
        port = default_port
    else:
        print(f"Port {default_port} is in use, finding an available port...")
        port = find_free_port(default_port + 1)  # start checking from 8081
        if port:
            print(f"Starting server on port {port}")
        else:
            print("Letting OS pick an available port...")
            port = 0
    
    # start the server on the determined port
    server.start(port=port)

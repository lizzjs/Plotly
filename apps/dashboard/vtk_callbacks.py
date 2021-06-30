
import dash_vtk
from dash.dependencies import Input, Output
import floris.tools as wfct
import numpy as np
import random

import apps.floris_data
from app import app

# Initialize the FLORIS interface fi
fi = wfct.floris_interface.FlorisInterface(input_dict=apps.floris_data.default_input_dict)
fd = fi.get_flow_data()

# compute dimensions, origins and spacing based on flow data
origin = [axis.mean().round().astype(int) for axis in [fd.x, fd.y, fd.z]]
ranges = np.array([axis.ptp().round().astype(int) for axis in [fd.x, fd.y, fd.z]])
dimensions = np.array([np.unique(axis).shape[0] for axis in [fd.x, fd.y, fd.z]])
x, y, z = dimensions
spacing = np.round(ranges / dimensions).astype(int)

# Create the volumes
views = dict(u=fd.u, v=fd.v, w=fd.w)

def build_view_child(
    dimensions, spacing, origin, field, enabled, i, j, k, window, level
):
    slice_prop = {"colorWindow": window, "colorLevel": level}
    child = [
        dash_vtk.ShareDataSet(
            dash_vtk.ImageData(
                dimensions=dimensions,
                spacing=spacing,
                origin=origin,
                children=dash_vtk.PointData(
                    dash_vtk.DataArray(registration="setScalars", values=field)
                ),
            ),
        ),
    ]

    if "Volume" in enabled:
        child.append(
            dash_vtk.VolumeRepresentation(
                [dash_vtk.VolumeController(), dash_vtk.ShareDataSet()],
            )
        )
    if "i" in enabled:
        child.append(
            dash_vtk.SliceRepresentation(
                iSlice=int(round(i)),
                property=slice_prop,
                children=dash_vtk.ShareDataSet(),
            )
        )

    if "j" in enabled:
        child.append(
            dash_vtk.SliceRepresentation(
                jSlice=int(round(j)),
                property=slice_prop,
                children=dash_vtk.ShareDataSet(),
            )
        )

    if "k" in enabled:
        child.append(
            dash_vtk.SliceRepresentation(
                kSlice=int(round(k)),
                property=slice_prop,
                children=dash_vtk.ShareDataSet(),
            )
        )

    return child
@app.callback(
    Output("vtk-view", "children"),
    Output("vtk-view", "triggerRender"),
    Input("radio-dimension", "value"),
    Input("child-enabled", "value"),
    Input("color-window", "value"),
    Input("color-level", "value"),
    Input("slider-slice-i", "value"),
    Input("slider-slice-j", "value"),
    Input("slider-slice-k", "value"),
)
def update_flow_viz(
    selected_dim, enabled, window_coef, level_coef, slice_i, slice_j, slice_k
):
    field = views[selected_dim]
    window = (field.max() - field.min()) * window_coef
    level = (field.max() + field.min()) * level_coef

    new_view_child = build_view_child(
        dimensions,
        spacing,
        origin,
        window=window,
        level=level,
        field=field,
        enabled=enabled,
        i=slice_i,
        j=slice_j,
        k=slice_k,
    )
    return new_view_child, random.random()
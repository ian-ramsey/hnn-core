# Authors: Huzi Cheng <hzcheng15@icloud.com>
import numpy as np
import os.path as op

import hnn_core
from hnn_core import Dipole, Network, Params
from hnn_core.gui.gui import HNNGUI, init_network_from_widgets


def test_gui_load_params():
    """Test if gui loads default parameters properly"""
    gui = HNNGUI()

    assert isinstance(gui.params, Params)

    print(gui.params)
    print(gui.params['L2Pyr*'])


def test_gui_upload_params():
    """Test if gui handles uploaded parameters correctly"""
    gui = HNNGUI()
    _ = gui.run()

    params_name = 'default.json'
    hnn_core_root = op.join(op.dirname(hnn_core.__file__))
    params_fname = op.join(hnn_core_root, 'param', params_name)

    content = b""
    with open(params_fname, "rb") as f:
        for line in f:
            pass
            content += line
    uploaded_value = {
        params_name: {
            'metadata': {
                'name': params_name,
                'type': 'application/json',
                'size': len(content),
            },
            'content': content
        }
    }

    # change the default loaded parameters
    original_drive_count = len(gui.drive_widgets)
    assert original_drive_count > 0
    gui.delete_drive_button.click()
    assert len(gui.drive_widgets) == 0

    original_tstop = gui.tstop.value
    gui.tstop.value = 1

    # manually send uploaded content
    gui.load_button.set_trait('value', uploaded_value)

    # check if parameter is reloaded.
    assert gui.tstop.value == original_tstop
    assert len(gui.drive_widgets) == original_drive_count


def test_run_gui():
    """Test if main gui function gives proper ipywidget"""
    gui = HNNGUI()
    app_layout = gui.run()
    assert app_layout is not None
    gui.run_button.click()
    dpls = gui.variables['dpls']
    assert isinstance(gui.variables["net"], Network)
    assert isinstance(dpls, list)
    assert all([isinstance(dpl, Dipole) for dpl in dpls])


def test_gui_init_network():
    """Test if gui initializes network properly"""
    gui = HNNGUI()
    # now the default parameter has been loaded.
    init_network_from_widgets(gui.params, gui.tstep, gui.tstop, gui.variables,
                              gui.drive_widgets)

    # copied from test_network.py
    assert np.isclose(gui.variables['net']._inplane_distance, 1.)  # default
    assert np.isclose(gui.variables['net']._layer_separation, 1307.4)

# def test_gui_run_simulation():
#     """Test if gui can reproduce the same results as using hnn-core"""
#     pass

# def test_gui_update_simulation_parameters():
#     """Test if gui builds new network model after changing simulation
#     parameters."""
#     pass

# def test_gui_update_cell_connectivity():
#     """Test if gui builds new network model after changing simulation
#     parameters."""
#     pass

# def test_gui_update_drives():
#     """Test if gui builds new network model after changing simulation
#     parameters."""
#     pass

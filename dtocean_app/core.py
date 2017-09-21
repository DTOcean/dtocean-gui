
#    Copyright (C) 2016 Mathew Topper, Rui Duarte
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Set up logging
import logging
import warnings

module_logger = logging.getLogger(__name__)

import pickle

from PyQt4 import QtCore

from aneris.boundary.interface import (AutoInterface,
                                       MetaInterface) 
from aneris.control.data import DataStorage
from aneris.control.pipeline import Sequencer
from aneris.control.simulation import Controller, Loader

from dtocean_core import interfaces as core_interfaces
from dtocean_core.core import (Core,
                               Project,
                               AutoRaw,
                               AutoQuery,
                               AutoPlot,
                               AutoFileInput,
                               AutoFileOutput)
#from dtocean_core.menu import ConnectorMenu

from . import data as gui_data
from . import interfaces as gui_interfaces


class WidgetInterface(MetaInterface):

    """Interface with a widget"""

    def __init__(self):

        super(WidgetInterface, self).__init__()
        self.parent = None

        return


class InputWidgetInterface(WidgetInterface):

    """Interface for the dynnamic input widget"""
    
    
class OutputWidgetInterface(WidgetInterface):

    """Interface for the dynnamic output widget"""


class AutoInput(AutoInterface, InputWidgetInterface):
    
    def __init__(self):

        AutoInterface.__init__(self)
        InputWidgetInterface.__init__(self)
        
        return
        
    @classmethod
    def get_connect_name(cls):
        
        return "auto_input"
        
        
class AutoOutput(AutoInterface, OutputWidgetInterface):
    
    def __init__(self):

        AutoInterface.__init__(self)
        OutputWidgetInterface.__init__(self)
        
        return
        
    @classmethod
    def get_connect_name(cls):
        
        return "auto_output"
        

class GUIProject(QtCore.QObject, Project):
    
    # PyQt signals
    sims_updated = QtCore.pyqtSignal(object)
    active_index_changed = QtCore.pyqtSignal(str)
    
    '''Project class with signals'''
    
    def __init__(self, title):
        
        QtCore.QObject.__init__(self)
        Project.__init__(self, title)
        
        return
    
    def add_simulation(self, simulation, set_active=False):
        
        super(GUIProject, self).add_simulation(simulation, set_active)
        
        active_sim_title = self.get_simulation_title()
        self.active_index_changed.emit(active_sim_title)
        
        return
        
    def _set_active_index(self, index):
        
        super(GUIProject, self)._set_active_index(index)
        
        active_sim_title = self.get_simulation_title()
        self.active_index_changed.emit(active_sim_title)
        
        return
    
    def _set_simulation(self, simulation, index=None):

        index = super(GUIProject, self)._set_simulation(simulation, index)
        
        self.sims_updated.emit(self)
        
        return index
        
    def _dump(self):
        
        new_project = Project(self.title)
        
        new_project._pool = self._pool
        new_project._simulations = self._simulations
        new_project._active_index = self._active_index
        new_project._db_cred = self._db_cred
        
        return new_project
        
    def _load(self, project):
        
        self.title = project.title
        self._pool = project._pool
        self._simulations = project._simulations
        self._active_index = project._active_index
        self._db_cred = project._db_cred
        
        return


class GUICore(QtCore.QObject, Core):

    '''Class to initiate and manipulate projects with a GUI environment.
    '''

    # PyQt signals
    status_updated = QtCore.pyqtSignal()
    pipeline_reset = QtCore.pyqtSignal()
    
    # Extend the sockets for widgets
    _ext_sockets = ("FileInputInterface",
                    "FileOutputInterface",
                    "QueryInterface",
                    "RawInterface",
                    "PlotInterface",
                    "InputWidgetInterface",
                    "OutputWidgetInterface")

    # Extend the auto classes for widgets
    _auto_classes = (AutoInput,
                     AutoOutput,
                     AutoFileInput,
                     AutoFileOutput,
                     AutoPlot,
                     AutoRaw,
                     AutoQuery)
                                          
    def __init__(self):
        
        QtCore.QObject.__init__(self)
        Core.__init__(self)
        self._input_parent = None
        
        return

    def _create_control(self):
        
        """Overload the structures base class"""
        
        data_store = DataStorage(gui_data, super_cls="GUIStructure")
        sequencer = Sequencer(self._hub_sockets,
                              core_interfaces)
        
        loader = Loader(data_store)
        control = Controller(data_store,
                             sequencer)

        return loader, control
        
    def new_project(self, project_title, simulation_title="Default"):
        
        new_project = GUIProject(project_title)
        self.new_simulation(new_project, simulation_title)
        
        return new_project
        
    def dump_project(self, project, dump_path):
        
        core_project = project._dump()
        
        super(GUICore, self).dump_project(core_project, dump_path)
        
        return
        
    def load_project(self, load_path):
        
        core_project = super(GUICore, self).load_project(load_path)
        
        gui_project = GUIProject("temp")
        gui_project._load(core_project)
        
        return gui_project
        
    def set_input_parent(self, widget):
        
        self._input_parent = widget
        
        return
        
    def reset_level(self, project,
                          level=None,
                          preserve_level=False,
                          force_scheduled=None,
                          skip_missing=False):
                              
        '''Prepare the simulation for re-execution at the given level'''
        
        super(GUICore, self).reset_level(project,
                                         level,
                                         preserve_level,
                                         force_scheduled,
                                         skip_missing)
        
        self.pipeline_reset.emit()
        
        return
        
    def set_interface_status(self, project, simulation=None):
        
        """Emit a signal on status update"""
                
        super(GUICore, self).set_interface_status(project, simulation)
        self.status_updated.emit()

        return
        
    def connect_interface(self, project, interface):
        
        """Add parent widget to widget interfaces"""
        
        if (isinstance(interface, InputWidgetInterface) and
           self._input_parent is not None):
            
            interface.parent = self._input_parent
            
        interface = super(GUICore, self).connect_interface(project, interface)
        
        return interface
        
    def _build_named_socket(self, socket_str):
        
        socket = super(GUICore, self)._build_named_socket(socket_str)
        socket.discover_interfaces(gui_interfaces)

        return socket


#class HubMenu(ConnectorMenu):
#    
#    def __init__(self, hub_name):
#        
#        super(HubMenu, self).__init__()
#        self._hidden_hub_name = hub_name
#    
#    @property
#    def _hub_name(self):
#        
#        return self._hidden_hub_name


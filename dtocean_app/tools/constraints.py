
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

module_logger = logging.getLogger(__name__)

from dtocean_core.tools.constraints import ConstraintsTool, plot_constraints

from . import GUITool
from ..widgets.display import MPLWidget


class GUIConstraintsTool(GUITool, ConstraintsTool):
    
    """A basic strategy which will run all selected modules and themes in
    sequence."""
    
    def __init__(self):
        
        ConstraintsTool.__init__(self)
        GUITool.__init__(self)
        
        return
    
    def connect(self, **kwargs):
        
        print "Calling plot"
        
        fig = plot_constraints(self.data)
        
        print "Made plot"
        
        self._widget = MPLWidget(fig)

        return

        


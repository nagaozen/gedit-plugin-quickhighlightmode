# -*- coding: utf-8 -*-

# gEdit QuickHighlightMode plugin
# Copyright (C) 2011 Fabio Zendhi Nagao
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gedit
from windowhelper import WindowHelper

class QuickHighlightModePlugin(gedit.Plugin):
    
    WINDOW_DATA_KEY = "QuickHighlightModePluginWindowData"
    
    def __init__(self):
        gedit.Plugin.__init__(self)
        
        self._popup_size = (450, 300)
    
    def activate(self, window):
        helper = WindowHelper(window, self)
        window.set_data(self.WINDOW_DATA_KEY, helper)
    
    def deactivate(self, window):
        window.get_data(self.WINDOW_DATA_KEY).deactivate()
        window.set_data(self.WINDOW_DATA_KEY, None)
    
    def update_ui(self, window):
        window.get_data(self.WINDOW_DATA_KEY).update_ui()
    
    def get_popup_size(self):
        return self._popup_size
    
    def set_popup_size(self, size):
        self._popup_size = size
    

# ex:ts=4:et:


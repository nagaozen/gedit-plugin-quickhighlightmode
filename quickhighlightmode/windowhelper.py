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
import gtk
from popup import Popup

# See /usr/share/gedit-2/ui/gedit-ui.xml
ui_str = """
<ui>
    <menubar name="MenuBar">
        <menu name="ViewMenu" action="View">
            <menuitem name="QuickHighlightMode" action="QuickHighlightMode"/>
        </menu>
    </menubar>
</ui>
"""

class WindowHelper:
    
    def __init__(self, window, plugin):
        self._window = window
        self._plugin = plugin
        self._popup = None
        
        self._install_menu()

    def deactivate(self):
        self._uninstall_menu()
        
        self._window = None
        self._plugin = None

    def update_ui(self):
        pass
    
    def _install_menu(self):
        manager = self._window.get_ui_manager()
        self._action_group = gtk.ActionGroup("GeditQuickHighlightModePluginActions")
        self._action_group.add_actions([(
            "QuickHighlightMode",
            gtk.STOCK_OPEN,
            _("Quick Highlight Mode"),
            "<Ctrl><Shift>H",
            _("Quickly switch between document syntax highlight modes"),
            self.on_lang_switcher_activate
        )])
        
        manager.insert_action_group(self._action_group, -1)
        self._ui_id = manager.add_ui_from_string(ui_str)
    
    def _uninstall_menu(self):
        manager = self._window.get_ui_manager()
        
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        
        manager.ensure_update()
    
    def _create_popup(self):
        self._popup = Popup(self._window, self.on_selected)
        
        self._popup.set_default_size(*self._plugin.get_popup_size())
        self._popup.set_transient_for(self._window)
        self._popup.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        
        self._window.get_group().add_window(self._popup)
        
        self._popup.connect("destroy", self._destroy_popup)
    
    def _destroy_popup(self, popup):
        alloc = popup.get_allocation()
        self._plugin.set_popup_size((alloc.width, alloc.height))
        
        self._popup = None
    
    # Events
    def on_lang_switcher_activate(self, action):
        if not self._popup:
            self._create_popup()
        
        self._popup.show()
    
    def on_selected(self, lang):
        doc = self._window.get_active_document()
        doc.set_language(lang)
        return True
    

# ex:ts=4:et:


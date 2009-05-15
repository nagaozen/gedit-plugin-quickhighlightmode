#!/usr/bin/python
# 
# Quick Highlight Mode
# ====================
# 
# This plugin provides a faster and easier way to select the current document
# highlighting mode. Just press Ctrl+Shift+H, type the language and press Enter.
# 
# Credits
# -------
# 
# Quick Highlight Mode was originally developed by [Nando Vieira](http://simplesideias.com.br/)
# but since he left this project development leaving some unfixed bugs, it has been touched by
# [Fabio Zendhi Nagao](http://zend.lojcomm.com.br/).
# 
# License
# -------
# 
# Copyright (C) 2009 [Fabio Zendhi Nagao](http://zend.lojcomm.com.br/)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
# 
# Changes
# -------
# 
# > @2009-04-10
# > I'm currently working to rewrite the entire plugin following the PythonPluginHowTo
# > suggested structure for an easier and better open source contribution. Also I'm fixing the bugs wherever I found them.

from gettext import gettext as _

import os
import os.path
import gtk
import gtk.glade
import gedit

GLADE_FILE = os.path.join(os.path.dirname(__file__), "quickhighlightmode.glade")

QUICKHIGHLIGHTMODE_MENU_UI_STR = """
<ui>
    <menubar name="MenuBar">
        <menu name="ViewMenu" action="View">
            <placeholder name="QuickHighlightModePluginPlaceHolder" />
            <menuitem name="QuickHighlightMode" action="QuickHighlightMode"/>
        </menu>
    </menubar>
</ui>
"""

class QuickHighlightModeWindowHelper(object):
    def __init__(self, plugin, window):
        self.window = window
        self.dialog = None
        self.language_manager = gedit.get_language_manager()
        self.available_langs = {}
        self.model = gtk.ListStore(str)
        self.model.set_sort_column_id(0, gtk.SORT_ASCENDING)
        
        self._populate()
        self._insert_menu()
    
    def deactivate(self):
        self._remove_menu()
        
        self.model = None
        self.language_manager = None
        self.dialog = None
        self.window = None
    
    def update_ui(self):
        self._action_group.set_sensitive(self.window.get_active_document() != None)
    
    def on_close(self, *args):
        self._close_dialog()
    
    def on_selected(self, completion, model, iter):
        lang = model.get_value(iter, 0)
        self._set_language(lang)
    
    def on_cancel(self, *args):
        self._close_dialog()
    
    def on_apply(self, *args):
        lang = self.entry.get_text()
        self._set_language(lang)
    
    def _populate(self):
        self.available_langs["Plain Text"] = None
        self.model.append(["Plain Text"])
        
        langs = self.language_manager.get_language_ids()
        for id in langs:
            lang = self.language_manager.get_language(id)
            name = lang.get_name()
            
            self.available_langs[name] = lang
            self.model.append([name])
    
    def _insert_menu(self):
        self._action_group = gtk.ActionGroup("QuickHighlightModeActions")
        self._action_group.add_actions([('QuickHighlightMode', gtk.STOCK_SELECT_COLOR, _('Quick Highlight Mode'), '<Control><Shift>h', _("Press Ctrl+Shift+H for quick highlight mode"), self._open_dialog)], self.window)
        
        manager = self.window.get_ui_manager()
        manager.insert_action_group(self._action_group, -1)
        self._ui_id = manager.add_ui_from_string(QUICKHIGHLIGHTMODE_MENU_UI_STR)
    
    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()
        
        self._action_group = None
    
    def _open_dialog(self, *args):
        glade_xml = gtk.glade.XML(GLADE_FILE)
        
        if self.dialog:
            self.dialog.set_focus(True)
            return
        
        self.dialog = glade_xml.get_widget('quickhighlightmode_dialog')
        self.dialog.connect('delete_event', self.on_close)
        self.dialog.show_all()
        self.dialog.set_transient_for(self.window)
        
        combobox = glade_xml.get_widget('language_list')
        combobox.set_model(self.model)
        combobox.set_text_column(0)
        
        entry_completion = gtk.EntryCompletion()
        entry_completion.connect('match-selected', self.on_selected)
        entry_completion.set_model(self.model)
        entry_completion.set_text_column(0)
        
        self.entry = combobox.get_children()[0]
        self.entry.set_completion(entry_completion)
        
        button_cancel = glade_xml.get_widget('cancel_button')
        button_cancel.connect('clicked', self.on_cancel)
        
        button_apply = glade_xml.get_widget('apply_button')
        button_apply.connect('clicked', self.on_apply)
    
    def _close_dialog(self):
        self.dialog.destroy()
        self.dialog = None
    
    def _set_language(self, lang):
        lang = self.available_langs[lang]
        doc = self.window.get_active_document()
        doc.set_language(lang)
        
        self._close_dialog()

class QuickHighlightModePlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}
    
    def activate(self, window):
        self._instances[window] = QuickHighlightModeWindowHelper(self, window)
    
    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]
    
    def update_ui(self, window):
        self._instances[window].update_ui()

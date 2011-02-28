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
import gobject
import gtk
import gtk.gdk
import gtksourceview2
import pango

class Popup(gtk.Dialog):
    
    def __init__(self, window, handler):
        gtk.Dialog.__init__(
            self,
            title=_('Quick Highlight Mode'),
            parent=window,
            flags=gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR | gtk.DIALOG_MODAL
        )
        
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self._ok_button = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        
        self._lang_manager = gtksourceview2.LanguageManager()
        self._lang_ids     = self._lang_manager.get_language_ids()
        self._handler      = handler
        self._cursor       = None
        
        self._build_ui()
        
        ag = gtk.AccelGroup()
        ag.connect_group(gtk.keysyms.l, gtk.gdk.CONTROL_MASK, 0, self.on_focus_entry)
        
        self.add_accel_group(ag)
    
    def _build_ui(self):
        vbox = self.get_content_area()
        vbox.set_spacing(3)
        
        self._entry = gtk.Entry()
        self._entry.connect("changed", self.on_entry_changed)
        self._entry.connect("key-press-event", self.on_entry_key_press_event)
        
        sw = gtk.ScrolledWindow(None, None)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_OUT)
        
        self._tv = gtk.TreeView()
        self._tv.set_headers_visible(False)
        self._tv.connect('row-activated', self.on_tv_row_activated)
        
        self._ls = gtk.ListStore(str, object)
        self._ls.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self._tv.set_model(self._ls)
        
        tvc = gtk.TreeViewColumn()
        crt = gtk.CellRendererText()
        tvc.pack_start(crt, True)
        tvc.set_attributes(crt, markup=0)
        tvc.set_cell_data_func(crt, self._cellrenderer)
        
        self._tv.append_column(tvc)
        sw.add(self._tv)
        
        selection = self._tv.get_selection()
        selection.connect("changed", self.on_tv_selection_changed)
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        
        vbox.pack_start(self._entry, False, False, 0)
        vbox.pack_start(sw, True, True, 0)
        
        # Initial selection
        self.on_tv_selection_changed(self._tv.get_selection())
        vbox.show_all()
    
    def _cellrenderer(self, tvc, crt, ls, piter):
        path = ls.get_path(piter)
        
        if self._cursor and path == self._cursor.get_path():
            style = self._tv.get_style()
            bg = style.bg[gtk.STATE_PRELIGHT]
            
            crt.set_property("cell-background-gdk", bg)
            crt.set_property("style", pango.STYLE_ITALIC)
        else:
            crt.set_property("cell-background-set", False)
            crt.set_property("style-set", False)
    
    def make_markup(self, prefix, lang_id):
        return "<b>%s</b>%s"%(prefix,lang_id[len(prefix):])
    
    def _append_to_store(self, item):
        self._ls.append(item)
    
    def _clear_store(self):
        self._ls.clear()
    
    def _append_all_langs(self):
        for l in self._lang_ids:
            self._append_to_store( ( l, self._lang_manager.get_language(l) ) )
    
    def _direct_lang(self):
        lang = None
        
        name = self._entry.get_text().strip()
        if name in self._lang_ids:
            lang = self._lang_manager.get_language(name)
        
        return lang
    
    def _activate(self):
        model, rows = self._tv.get_selection().get_selected_rows()
        ret = True
        
        for row in rows:
            piter = model.get_iter(row)
            lang = model.get(piter, 1)[0]
            ret = ret and self._handler(lang)
        
        if rows and ret:
            self.destroy()
        
        if not rows:
            lang = self._direct_lang()
            if lang and self._handler(lang):
                self.destroy()
            else:
                ret = False
        else:
            ret = False
        
        return ret
    
    # Predefined signal handlers
    def do_show(self):
        gtk.Window.do_show(self)
        
        self._entry.grab_focus()
        self._entry.set_text('')
        
        self.do_search()
    
    def do_response(self, response):
        if response != gtk.RESPONSE_ACCEPT or not self._activate():
            self.destroy()
    
    def do_search(self):
        self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        self._remove_cursor()
        
        text = self._entry.get_text().strip()
        self._clear_store()
        
        if text == '':
            self._append_all_langs()
        else:
            for l in self._lang_ids:
                if l.startswith(text):
                    self._append_to_store( ( self.make_markup(text, l), self._lang_manager.get_language(l) ) )
        
        piter = self._ls.get_iter_first()
        
        if piter:
            self._tv.get_selection().select_path(self._ls.get_path(piter))
        
        self.window.set_cursor(None)
    
    # Cursor stuff
    def _remove_cursor(self):
        if self._cursor:
            path = self._cursor.get_path()
            self._cursor = None
            
            self._ls.row_changed(path, self._ls.get_iter(path))
    
    def _toggle_cursor(self):
        if not self._cursor:
            return
        
        path = self._cursor.get_path()
        selection = self._tv.get_selection()
        
        if selection.path_is_selected(path):
            selection.unselect_path(path)
        else:
            selection.select_path(path)
    
    def _shift_extend(self, towhere):
        selection = self._tv.get_selection()
        
        if not self._shift_start:
            model, rows = selection.get_selected_rows()
            start = rows[0]
        
            self._shift_start = gtk.TreeRowReference(self._ls, start)
        else:
            start = self._shift_start.get_path()
        
        selection.unselect_all()
        selection.select_range(start, towhere)
    
    def _select_index(self, idx, hasctrl, hasshift):
        path = (idx,)
        
        if not (hasctrl or hasshift):
            self._tv.get_selection().unselect_all()
        
        if hasshift:
            self._shift_extend(path)
        else:
            self._shift_start = None
            
            if not hasctrl:
                self._tv.get_selection().select_path(path)
        
        self._tv.scroll_to_cell(path, None, True, 0.5, 0)
        self._remove_cursor()
        
        if hasctrl or hasshift:
            self._cursor = gtk.TreeRowReference(self._ls, path)
            
            piter = self._ls.get_iter(path)
            self._ls.row_changed(path, piter)
    
    def _move_selection(self, howmany, hasctrl, hasshift):
        num = self._ls.iter_n_children(None)
        
        if num == 0:
            return True
        
        # Test for cursor
        path = None
        
        if self._cursor:
            path = self._cursor.get_path()
        else:
            model, rows = self._tv.get_selection().get_selected_rows()
            
            if len(rows) == 1:
                path = rows[0]
        
        if not path:
            if howmany > 0:
                self._select_index(0, hasctrl, hasshift)
            else:
                self._select_index(num - 1, hasctrl, hasshift)
        else:
            idx = path[0]
            
            if idx + howmany < 0:
                self._select_index(0, hasctrl, hasshift)
            elif idx + howmany >= num:
                self._select_index(num - 1, hasctrl, hasshift)
            else:
                self._select_index(idx + howmany, hasctrl, hasshift)
        
        return True
    
    # Events
    def on_focus_entry(self, group, accel, keyval, modifier):
        self._entry.grab_focus()
    
    def on_entry_changed(self, editable):
        self.do_search()
        self.on_tv_selection_changed(self._tv.get_selection())
    
    def on_entry_key_press_event(self, widget, event):
        move_mapping = {
            gtk.keysyms.Down: 1,
            gtk.keysyms.Up: -1,
            gtk.keysyms.Page_Down: 5,
            gtk.keysyms.Page_Up: -5
        }
        
        if event.keyval == gtk.keysyms.Escape:
            self.destroy()
            return True
        elif event.keyval in move_mapping:
            return self._move_selection(move_mapping[event.keyval], event.state & gtk.gdk.CONTROL_MASK, event.state & gtk.gdk.SHIFT_MASK)
        elif event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter, gtk.keysyms.Tab, gtk.keysyms.ISO_Left_Tab]:
            return self._activate()
        elif event.keyval == gtk.keysyms.space and event.state & gtk.gdk.CONTROL_MASK:
            self._toggle_cursor()
        
        return False
    
    def on_tv_row_activated(self, view, path, column):
        self._activate()
    
    def on_tv_selection_changed(self, selection):
        model, rows = selection.get_selected_rows()
        
        lang = None
        
        if not rows:
            lang = self._direct_lang()
        elif len(rows) == 1:
            lang = model.get(model.get_iter(rows[0]), 1)[0]
        
        self._ok_button.set_sensitive( lang != None )
    

gobject.type_register(Popup)

# ex:ts=4:et:


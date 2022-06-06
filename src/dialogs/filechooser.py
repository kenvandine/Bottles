# filechooser.py
#
# Copyright 2020 brombinmirko <send@mirko.pm>
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

from gi.repository import Gtk, Adw


class FileChooser:

    def __init__(self, parent, title, action, buttons, path=None, filters=None, native=True, callback=None):
        self.parent = parent
        self.title = title
        self.action = action
        self.path = path
        self.native = native
        self.callback = callback
        self.buttons = self.__get_buttons(buttons)
        self.filters = self.__get_filters(filters)

        self.__build_dialog()

    def __build_dialog(self):
        if self.native:
            dialog = Gtk.FileChooserNative.new(self.title, self.parent, self.action, self.buttons[0], self.buttons[1])
        else:
            dialog = Gtk.FileChooserDialog(title=self.title, action=self.action)
            dialog.add_buttons(*self.buttons)
            if self.path:
                dialog.set_current_folder(self.path)

        dialog.set_modal(True)
        dialog.set_transient_for(self.parent)

        if self.filters:
            for f in self.filters:
                dialog.add_filter(f)

        if self.callback:
            dialog.connect('response', self.callback, dialog)

        dialog.show()

    def __get_buttons(self, buttons):
        if buttons is None:
            buttons = _("Cancel", _("Save"))

        if self.native:
            return buttons

        return buttons[0], Gtk.ResponseType.CANCEL, buttons[1], Gtk.ResponseType.OK

    @staticmethod
    def __get_filters(filters):
        _filters = []

        if filters is None:
            return _filters

        for f in filters:
            _filter = Gtk.FileFilter()
            _filter.set_name(f)
            _filter.add_pattern(f"*.{f}")
            _filters.append(_filter)

        return _filters

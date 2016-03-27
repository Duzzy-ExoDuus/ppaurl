#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# preferences_dialog.py
#
# This file is part of 2gif
#
# Copyright (C) 2016
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
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

import gi
from gi.repository import Gtk
import comun
import os
import shutil
from comun import _
from configurator import Configuration
from backlight import BacklightManager
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(1)


class PreferencesDialog(Gtk.Dialog):
    def __init__(self):
        #
        Gtk.Dialog.__init__(self,
                            'Backlight Indicator | '+_('Preferences'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                                Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect('close', self.close_ok)
        self.set_icon_from_file(comun.ICON)
        #
        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.get_content_area().add(vbox0)
        # ***************************************************************
        notebook = Gtk.Notebook.new()
        vbox0.add(notebook)
        # ***************************************************************
        vbox11 = Gtk.VBox(spacing=5)
        vbox11.set_border_width(5)
        notebook.append_page(vbox11, Gtk.Label.new(_('General')))
        frame11 = Gtk.Frame()
        vbox11.pack_start(frame11, False, True, 1)
        table11 = Gtk.Table(2, 2, False)
        frame11.add(table11)
        # ***************************************************************
        label11 = Gtk.Label(_('Autostart')+':')
        label11.set_alignment(0, 0.5)
        table11.attach(label11, 0, 1, 0, 1, xpadding=5, ypadding=5)
        self.switch1 = Gtk.Switch()
        table11.attach(self.switch1, 1, 2, 0, 1,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label12 = Gtk.Label(_('Icon light')+':')
        label12.set_alignment(0, 0.5)
        table11.attach(label12, 0, 1, 1, 2, xpadding=5, ypadding=5)
        self.switch2 = Gtk.Switch()
        table11.attach(self.switch2, 1, 2, 1, 2,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        # ***************************************************************
        hbox2 = Gtk.HBox(spacing=5)
        hbox2.set_border_width(5)
        notebook.append_page(hbox2, Gtk.Label.new(_('Backlight')))
        frame2 = Gtk.Frame()
        hbox2.pack_start(frame2, False, True, 1)
        table2 = Gtk.Table(4, 2, False)
        frame2.add(table2)
        # ***************************************************************
        label21 = Gtk.Label(_('Minimum backlight')+':')
        label21.set_alignment(0, 0.5)
        table2.attach(label21, 0, 1, 0, 1,
                      xpadding=5, ypadding=5)
        adjustment1 = Gtk.Adjustment(0, 0, 101, 5, 10, 1)
        self.minimum_backlight = Gtk.Scale()
        self.minimum_backlight.set_digits(0)
        self.minimum_backlight.set_size_request(200, 10)
        self.minimum_backlight.set_adjustment(adjustment1)
        self.minimum_backlight.connect('value-changed',
                                       self.on_minimum_backlight_changed)
        table2.attach(self.minimum_backlight, 1, 2, 0, 1,
                      xpadding=5, ypadding=5)
        label22 = Gtk.Label(_('Maximum backlight')+':')
        label22.set_alignment(0, 0.5)
        table2.attach(label22, 0, 1, 1, 2,
                      xpadding=5, ypadding=5)
        adjustment2 = Gtk.Adjustment(100, 0, 101, 5, 10, 1)
        self.maximum_backlight = Gtk.Scale()
        self.maximum_backlight.set_digits(0)
        self.maximum_backlight.set_size_request(200, 10)
        self.maximum_backlight.set_adjustment(adjustment2)
        self.maximum_backlight.connect('value-changed',
                                       self.on_maximum_backlight_changed)
        table2.attach(self.maximum_backlight, 1, 2, 1, 2,
                      xpadding=5, ypadding=5)
        label23 = Gtk.Label(_('Backlight')+':')
        label23.set_alignment(0, 0.5)
        table2.attach(label23, 0, 1, 2, 3,
                      xpadding=5, ypadding=5)
        adjustment3 = Gtk.Adjustment(50, 0, 101, 5, 10, 1)
        self.backlight = Gtk.Scale()
        self.backlight.set_digits(0)
        self.backlight.set_size_request(200, 10)
        self.backlight.set_adjustment(adjustment3)
        self.backlight.connect('value-changed', self.on_backlight_changed)
        table2.attach(self.backlight, 1, 2, 2, 3,
                      xpadding=5, ypadding=5)
        label24 = Gtk.Label(_('Sample time')+' ('+_('min')+'):')
        label24.set_alignment(0, 0.5)
        table2.attach(label24, 0, 1, 3, 4,
                      xpadding=5, ypadding=5)
        adjustment4 = Gtk.Adjustment(5, 0, 121, 1, 5, 1)
        self.sample_time = Gtk.SpinButton()
        self.sample_time.set_size_request(200, 10)
        self.sample_time.set_adjustment(adjustment4)
        table2.attach(self.sample_time, 1, 2, 3, 4,
                      xpadding=5, ypadding=5, xoptions=Gtk.AttachOptions.FILL)
        #
        self.load_preferences()
        #
        self.show_all()

    def close_ok(self):
        self.save_preferences()

    def load_preferences(self):
        configuration = Configuration()
        first_time = configuration.get('first-time')
        version = configuration.get('version')
        if first_time or version != comun.VERSION:
            configuration.set_defaults()
            configuration.read()
        self.switch1.set_active(os.path.exists(comun.AUTOSTARTD))
        self.switch2.set_active(configuration.get('theme') == 'light')
        self.minimum_backlight.set_value(
            configuration.get('minimum-backlight'))
        self.maximum_backlight.set_value(
            configuration.get('maximum-backlight'))
        self.backlight.set_value(configuration.get('backlight'))
        self.sample_time.set_value(configuration.get('sample-time'))

    def save_preferences(self):
        configuration = Configuration()
        configuration.set('first-time', False)
        configuration.set('version', comun.VERSION)
        create_or_remove_autostart(self.switch1.get_active())
        if self.switch2.get_active() is True:
            configuration.set('theme', 'light')
        else:
            configuration.set('theme', 'dark')
        configuration.set('minimum-backlight',
                          self.minimum_backlight.get_value())
        configuration.set('maximum-backlight',
                          self.maximum_backlight.get_value())
        configuration.set('backlight',
                          self.backlight.get_value())
        configuration.set('sample-time',
                          self.sample_time.get_value())
        configuration.save()

if __name__ == "__main__":
    cm = PreferencesDialog()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        print(1)
        cm.close_ok()
    cm.hide()
    cm.destroy()
    exit(0)

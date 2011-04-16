#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class MainWindow(object):

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        self.db.close()
        gtk.main_quit()
        return False

    def __init__(self, db):
        self.db = db

        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Basic TreeView Example")
        self.window.set_size_request(800, 600)
        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.store = gtk.ListStore(str, str)
        # we'll add some data now - 4 rows with 3 child rows each
        for game in self.db:
            s = "<span font_weight='bold' size='medium'>%s</span>\n<span size='x-small'>by %s (%s)</span>" % (game.title, game.manufacturer, game.year)
            self.store.append([game.name, s])
        # create the TreeView using store
        self.treeview = gtk.TreeView(self.store)
        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Game')
        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)
        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()
        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)
        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in store
        self.tvcolumn.add_attribute(self.cell, 'markup', 1)
        # make it searchable
        self.treeview.set_search_column(1)
        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(1)
        # Allow drag and drop reordering of rows
        self.treeview.set_reorderable(False)
        self.window.add(self.treeview)

        self.window.show_all()

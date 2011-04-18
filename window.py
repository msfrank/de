#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from mame import MAME

class MainWindow(object):

    def __init__(self, db):
        # initialize keybindings
        self.KEY_QUIT = gtk.keysyms.q
        self.KEY_UP = gtk.keysyms.w
        self.KEY_DOWN = gtk.keysyms.s
        self.KEY_LEFT = gtk.keysyms.a
        self.KEY_RIGHT = gtk.keysyms.d
        self.KEY_SELECT = gtk.keysyms.Return
        self.KEY_RETURN = gtk.keysyms.Escape

        # hold onto db reference
        self.db = db

        # create a new MAME instance
        self.mame = MAME('/usr/games/mame')

        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("DOUBLE ELBOW!")
        self.window.set_size_request(800, 600)
        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.store = gtk.ListStore(str, str)
        # we'll add some data now - 4 rows with 3 child rows each
        for game in self.db:
            s = "<span font_weight='bold' size='medium'>%s</span>\n" % game.title
            s += "<span size='x-small'>by %s (%s)</span>" % (game.manufacturer, game.year)
            self.store.append([game.name, s])
        # create the TreeView using store
        self.treeview = gtk.TreeView(self.store)
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_search(False)
        self.treeview.set_reorderable(False)
        self.treeview.connect('key-press-event', self.key_nav)
        self.window.add(self.treeview)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Game')
        self.treeview.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'markup', 1)
        #self.tvcolumn.set_sort_column_id(1)

        # get a reference to the tree selection
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(gtk.SELECTION_SINGLE)
        self.selection.select_path((0,))

        self.window.show_all()

    def delete_event(self, window, event, data=None):
        self.db.close()
        gtk.main_quit()
        return False

    def key_nav(self, window, event):
        print "key_nav: %s" % str(event)
        # quit application
        if event.keyval == self.KEY_QUIT:
            return self.delete_event(window, event)
        # select previous game
        if event.keyval == self.KEY_UP:
            model,item = self.selection.get_selected()
            path = self.store.get_path(item)
            if path[0] > 0:
                path = (path[0] - 1,)
                self.selection.unselect_all()
                self.selection.select_path(path)
                self.treeview.set_cursor(path)
        # select next game
        if event.keyval == self.KEY_DOWN:
            model,item = self.selection.get_selected()
            item = self.store.iter_next(item)
            if not item == None:
                self.selection.unselect_all()
                self.selection.select_iter(item)
                path = self.store.get_path(item)
                self.treeview.set_cursor(path)
        # play selected game
        if event.keyval == self.KEY_SELECT:
            model,item = self.selection.get_selected()
            name = str(self.store.get(item, 0)[0])
            print "running game: %s" % name
            game = self.db[name]
            proc = self.mame.play(game)
        return True


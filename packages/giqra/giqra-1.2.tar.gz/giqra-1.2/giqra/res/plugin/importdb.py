import pathlib
from iqra import db
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


N_ = lambda x: x
N_('importdb')

def connect_signals(builder, obj, signal_name, handler_name, connect_object,
        flags, plugin, util):
    obj.connect(signal_name, globals()[handler_name], builder, plugin, util)

def on_guess_version_checkbutton_toggled(button, builder, plugin, util):
    builder.get_object('version_spinbutton').set_sensitive(
        not button.get_active())

def on_choose_file_button_clicked(button, builder, plugin, util):
    dialog = builder.get_object('open_dialog')
    dialog.set_current_name('')
    result = dialog.run()
    dialog.hide()
    if result == Gtk.ResponseType.OK:
        builder.get_object('file_entry').set_text(dialog.get_filename())

def init_ui(builder):
    builder.get_object('guess_version_checkbutton').set_active(True)
    builder.get_object('library_checkbutton').set_active(True)
    builder.get_object('author_checkbutton').set_active(True)
    builder.get_object('publisher_checkbutton').set_active(True)
    builder.get_object('section_checkbutton').set_active(True)
    builder.get_object('book_checkbutton').set_active(True)
    builder.get_object('borrow_checkbutton').set_active(True)

def start(builder, main_win):
    dialog = builder.get_object('start_dialog')
    dialog.set_transient_for(main_win)
    
    init_ui(builder)
    
    result = dialog.run()
    dialog.hide()
    
    exclude = []
    update = []
    if result == Gtk.ResponseType.OK:
        if builder.get_object('guess_version_checkbutton').get_active():
            version = None
        else:
            version = builder.get_object(
                'version_spinbutton').get_value_as_int()
        if not builder.get_object('library_checkbutton').get_active():
            exclude.append(db.Library)
        else:
            update.append('library')
        if not builder.get_object('author_checkbutton').get_active():
            exclude.append(db.Author)
        else:
            update.append('author')
        if not builder.get_object('publisher_checkbutton').get_active():
            exclude.append(db.Publisher)
        else:
            update.append('publisher')
        if not builder.get_object('section_checkbutton').get_active():
            exclude.append(db.Section)
        else:
            update.append('section')
        if not builder.get_object('book_checkbutton').get_active():
            exclude.append(db.Book)
        else:
            update.append('book')
        if not builder.get_object('borrow_checkbutton').get_active():
            exclude.append(db.Borrow)
        else:
            update.append('borrow')
        
        return update, tuple(), {
            'name': builder.get_object('file_entry').get_text(),
            'version': version,
            'exclude': exclude,
        }


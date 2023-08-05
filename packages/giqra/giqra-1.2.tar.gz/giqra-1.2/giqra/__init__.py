'''
:Date: 2019-11-20
:Version: 1.2
:Authors:
    * Mohammad Alghafli <thebsom@gmail.com>

GUI for iqra, the library management program.

------------
Installation
------------

giqra requires pygobject 3.20 or above. This library cannot be installed via pip. Make sure to install it. If you are using linux, install it from your package manager. If you are using windows, follow the instructions on https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started

After installing pygobject, on windows install giqra using pip by running the
command::
    
    pip install giqra

Or on linux::
    
    pip3 install giqra

All other dependancies will be installed automatically by pip.

-----
Usage
-----

Running the application::

    python3 -m giqra

Use -h option to know all the possible options::

    python3 -m giqra -h
'''

import sys
import sqlalchemy
import iqra
from iqra import db
import datetime
import pathlib
import random
import threading
import locale
import gettext
import importlib
import codi
from . import giqra_thread
from .gdict import GDict

if sys.platform == 'win32':
    import ctypes
    libintl = ctypes.cdll.LoadLibrary('libintl-8.dll')
    locale.bindtextdomain = libintl.bindtextdomain

def init(config_dir=None, profile='default'):
    global util, _, N_, configdirs, trans_dir, TRANSLATE_WIDGETS
    global Gtk, Gdk, GdkPixbuf, Gio, GLib, Pango
    
    util = iqra.IqraUtil(config_dir=None, profile=profile)

    module_path = pathlib.Path(__file__).resolve()
    if module_path.is_file():
        module_path = module_path.parent
    
    configdirs = [util.codi[0] / 'giqra', module_path]
    configdirs = codi.Codi(*configdirs)
    
    trans_dir = str(configdirs.path('res/translations/mo/'))
    N_ = lambda text: text
    _ = gettext.translation(
        'giqra', trans_dir, [util.get_config('language')], 
        fallback=True).gettext
    
    locale.bindtextdomain('giqra', trans_dir)

    import gi
    gi.require_version('Gtk', '3.0')

    from gi.repository import Gtk
    from gi.repository import Gdk
    from gi.repository import GdkPixbuf
    from gi.repository import Gio
    from gi.repository import GLib
    from gi.repository import Pango
    
    TRANSLATE_WIDGETS = {
            Gtk.Label: [('get_label', 'set_label')],
            Gtk.Button: [('get_label', 'set_label')],
            Gtk.TreeViewColumn: [('get_title', 'set_title')],
            Gtk.Stack: ['title'],
        }

def trans_ui(ui, trans_dir):
    if sys.platform == 'win32':
        print('doing translation workaround')
        trans = gettext.translation(
                ui.get_translation_domain(),
                trans_dir,
                [util.get_config('language')],
                fallback=True
            ).gettext
        
        for c in ui.get_objects():
            t = type(c)
            if t in TRANSLATE_WIDGETS:
                for d in TRANSLATE_WIDGETS[t]:
                    if type(d) is tuple:
                        getter, setter = d
                        orig = getattr(c, getter)()
                        if orig:
                            getattr(c, setter)(trans(orig))
                    else:
                        for e in c.get_children():
                            orig = c.child_get_property(e, d)
                            if orig:
                                c.child_set_property(e, d, trans(orig))

def config_set_value(widget, value):
    if isinstance(widget, Gtk.SpinButton):
        widget.set_value(value)
    elif isinstance(widget, Gtk.Entry):
        widget.set_text(value)
    elif isinstance(widget, Gtk.ColorButton):
        widget.set_rgba(Gdk.RGBA(*value))
    elif isinstance(widget, Gtk.FontButton):
        widget.set_font(value)
    elif isinstance(widget, Gtk.ListStore):
        widget.clear()
        for c in value:
            widget.append([c])
    elif isinstance(widget, Gtk.ComboBoxText):
        widget.set_active_id(value)
    elif isinstance(widget, Gtk.TextView):
        widget.get_buffer().set_text(value)
    else:
        print('could not set value to widget type `{}`'.format(type(widget)))

def config_get_value(widget):
    if isinstance(widget, Gtk.SpinButton):
        return widget.get_value()
    elif isinstance(widget, Gtk.Entry):
        return widget.get_text()
    elif isinstance(widget, Gtk.ColorButton):
        rgba = widget.get_rgba()
        return [rgba.red, rgba.green, rgba.blue]
    elif isinstance(widget, Gtk.FontButton):
        return widget.get_font()
    elif isinstance(widget, Gtk.ListStore):
        return [c[0] for c in widget]
    elif isinstance(widget, Gtk.ComboBoxText):
        value = widget.get_active_id()
        text = widget.get_active_text()
        if value is None:
            value = text
        return value
    elif isinstance(widget, Gtk.TextView):
        buf = widget.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
    else:
        print('could not get value from widget type `{}`'.format(type(widget)))

def populate_config(plugin):
    idx = 'plugin_{}_config'.format(load_plugin_ui(plugin))
    
    builder = ui[idx][0]
    if builder is not None:
        for c in plugin.CONFIG:
            widget = builder.get_object(c)
            if widget is not None:
                config_set_value(widget, util.get_config(c))

def on_plugin_start_clicked(button, plugin):
    idx = 'plugin_{}_config'.format(load_plugin_ui(plugin))
    
    args = load_plugin_py(plugin).start(ui[idx][0],
        ui['giqra'].get_object('main_win'))
    if args is not None:
        update, args, kwargs = args
        dialog = ui['giqra'].get_object('plugin_dialog')
        dialog.set_title(load_plugin_ui(plugin))
        dialog.plugin = plugin(util, step=on_plugin_step, end=on_plugin_end)
        ui['giqra'].get_object('plugin_progressbar').set_fraction(0)
        args = (dialog.plugin,) + args
        t = threading.Thread(target=plugin_call,
            args=args, kwargs=kwargs)
        t.start()
        result = dialog.run()
        dialog.hide()
        if result == Gtk.ResponseType.CANCEL:
            dialog.plugin.stop()
        
        if 'book' in update:
            populate_books_flowbox()
        if 'section' in update:
            populate_sections_treestore()
        if 'library' in update:
            populate_libraries_treestore()
        if 'author' in update:
            populate_authors_search_treestore()
        if 'publisher' in update:
            populate_publishers_search_treestore()
        if 'borrow' in update:
            populate_borrows_search_liststore()
        
        t.join()

def plugin_call(plugin, *args, **kwargs):
    try:
        plugin.call(*args, **kwargs)
    except Exception as e:
        print(repr(e))
        Gdk.threads_add_idle(GLib.PRIORITY_LOW, on_plugin_error, plugin, e)

def on_plugin_step(instance):
    progress = ui['giqra'].get_object('plugin_progressbar')
    Gdk.threads_add_idle(GLib.PRIORITY_LOW, progress.set_fraction,
        max(instance.ratio, 0))
    Gdk.threads_add_idle(GLib.PRIORITY_LOW, progress.set_text,
        '{} / {}'.format(instance.finished, instance.total))

def on_plugin_end(instance, response=None):
    if response is None:
        response = Gtk.ResponseType.OK
    
    dialog = ui['giqra'].get_object('plugin_dialog')
    dialog.plugin = None
    Gdk.threads_add_idle(GLib.PRIORITY_LOW, dialog.response, response)

def on_plugin_error(instance, e):
    dialog = Gtk.MessageDialog(ui['giqra'].get_object('plugin_dialog'),
        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
            _('An error occurred!'))
    dialog.format_secondary_text(type(e).__name__)
    dialog.run()
    dialog.destroy()
    on_plugin_end(instance, Gtk.ResponseType.REJECT)

def on_plugin_config_clicked(button, plugin):
    idx = 'plugin_{}_config'.format(load_plugin_ui(plugin))
    
    populate_config(plugin)
    dialog = ui[idx][1]
    if dialog.run() == Gtk.ResponseType.OK:
        apply_config(plugin)
    dialog.hide()

def load_plugin_ui(plugin):
    if hasattr(plugin, 'name'):
        name = plugin.name
    else:
        name = plugin.__name__
    
    idx = 'plugin_{}_config'.format(name)
    
    if idx not in ui:
        module_path = pathlib.Path(__file__).resolve().parent
        ui_path = module_path / 'res/plugin/glade/{}.glade'.format(name)
        trans_dir = module_path / 'res/plugin/translations/mo/'
        trans_domain = 'giqra.plugin.{}'.format(name)
        locale.bindtextdomain(trans_domain, trans_dir)
        plugin_ui = Gtk.Builder()
        plugin_ui.set_translation_domain(trans_domain)
        try:
            plugin_ui.add_from_file(str(ui_path))
            trans_ui(plugin_ui, trans_ui)
            try:
                dialog = Gtk.Dialog(_('{} Config').format(_(name)),
                    ui['giqra'].get_object('main_win'), 0,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
                dialog.get_content_area().pack_start(
                    plugin_ui.get_object('config'), True, True, 0)
            except Exception as e:
                print('could not create config dialog for plugin `{}`'.format(
                    name))
                dialog = None
            
            try:
                plugin_py = load_plugin_py(plugin)
                plugin_ui.connect_signals_full(
                    plugin_py.connect_signals, plugin, util)
            except Exception as e:
                print('could not load plugin py file')
                print(repr(e))
            
        except Exception as e:
            print('could not find glade file for plugin `{}`'.format(name))
            print(repr(e))
            plugin_ui = None
            dialog = None
        
        ui[idx] = [plugin_ui, dialog]
    
    return name

def load_plugin_py(plugin):
    if hasattr(plugin, 'name'):
        name = plugin.name
    else:
        name = plugin.__name__
    
    module_path = pathlib.Path(__file__).resolve().parent
    plugin_py_name =  '{}.res.plugin.{}'.format(module_path.name, name)
    return importlib.import_module(plugin_py_name)

def apply_config(plugin):
    if hasattr(plugin, 'name'):
        name = plugin.name
    else:
        name = plugin.__name__
    
    idx = 'plugin_{}_config'.format(name)
    for c in plugin.CONFIG:
        widget = ui[idx][0].get_object(c)
        if widget is not None:
            value = config_get_value(widget)
            t = type(plugin.CONFIG[c])
            util.set_config(c, t(value))

def gtk_call_wait(func, *args, **kwargs):
    e = threading.Event()
    Gdk.threads_add_idle(GLib.PRIORITY_LOW, func, *args, e, **kwargs)
    e.wait()

def populate_plugins():
    plugins = []
    for c in util.get_plugins():
        if hasattr(c, 'name'):
            name = c.name
        else:
            name = c.__name__
        
        module_path = pathlib.Path(__file__).resolve().parent
        trans_dir = module_path / 'res/plugin/translations/mo/'
        trans_domain = 'giqra.plugin.{}'.format(name)
        trans = gettext.translation(
            trans_domain, trans_dir, [util.get_config('language')], 
            fallback=True).gettext
        
        item = GDict()
        item['name'] = name
        item['plugin'] = c
        item['lname'] = trans(name)
        plugins.append(item)
    
    for c in sorted(plugins, key=lambda item: item['lname']):
        plugins_liststore.append(c)

def create_plugin_widget(item):
    box = Gtk.Box()
    label = Gtk.Label()
    label.set_markup('<span font="16 bold">{}</span>'.format(item['lname']))
    label.set_xalign(0)
    
    button_box = Gtk.Box(homogeneous=True)
    start_button = Gtk.Button.new_from_icon_name(
        'media-playback-start', Gtk.IconSize.DIALOG)
    start_button.connect('clicked', on_plugin_start_clicked, item['plugin'])
    config_button = Gtk.Button.new_from_icon_name(
        'gtk-preferences', Gtk.IconSize.DIALOG)
    config_button.connect('clicked', on_plugin_config_clicked, item['plugin'])
    
    try:
        plugin_py = load_plugin_py(item['plugin'])
        sensitive_start = True
    except Exception as e:
        print('could not find py file for plugin `{}`'.format(item['name']))
        sensitive_start = False
    
    idx = 'plugin_{}_config'.format(load_plugin_ui(item['plugin']))
    
    if ui[idx][1] is not None:
        sensitive_config = True
    else:
        sensitive_config = False
    
    start_button.set_sensitive(sensitive_start)
    config_button.set_sensitive(sensitive_config)
    
    button_box.pack_start(config_button, True, True, 0)
    button_box.pack_start(start_button, True, True, 0)
    
    box.pack_start(label, True, True, 0)
    box.pack_start(button_box, False, False, 0)
    box.show_all()
    return box

def clear_store(store, event):
    if issubclass(type(store), Gtk.TreeModel):
        store.clear()
        event.set()
    else:
        store.remove_all()
        event.set()

def append_to_treestore(treestore, parent, values, counter=None, event=None):
    if issubclass(type(treestore), Gtk.ListStore):
        treestore.append(values)
    else:
        treestore.append(parent, values)
    if counter is not None:
        counter['value'] -= 1
        if counter['value'] <= 0:
            event.set()

def call_count(f, counter=None, event=None, *args, **kwargs):
    f(*args, **kwargs)
    
    if counter is not None:
        counter['value'] -= 1
        if counter['value'] <= 0:
            event.set()

def get_treestore_column(treestore, column=1, idcolumn=0):
    #get current rows
    rows = {c[idcolumn]: c for c in treestore}
    
    new_rows = rows
    while new_rows:
        added_rows = {}
        for row in new_rows:
            added_rows.update(
                {c[idcolumn]: c for c in rows[row].iterchildren()}
            )
        rows.update(added_rows)
        new_rows = added_rows
    
    return {c: rows[c][column] for c in rows}

def get_thumb(id_, generate=True):
    THUMB_W = 128
    THUMB_H = 128
    
    try:
        thumb_path = util.get_thumbs(id_)[0]
    except IndexError:
        if generate:
            thumb_path = util.generate_thumb(id_)
        else:
            thumb_path = None
    except RuntimeError:
        thumb_path = None
    
    if thumb_path is not None:
        thumb = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(thumb_path),
            THUMB_W, THUMB_H, False)
    else:
        thumb = None
    
    return thumb

@giqra_thread.threadfun
def populate_sections_treestore(_event):
    session = util.get_scoped_session()
    
    label_template = '{0.number:0' + str(util.get_section_digits()) + '}-{0.name}'
    
    treestore = ui['giqra'].get_object('sections_treestore')
    
    search_active = get_treestore_column(treestore, 4)
    
    gtk_call_wait(clear_store, treestore)
    
    ids = [util.get_root_section(session).id]
    iters = {ids[0]: None}
    
    e = threading.Event()
    
    while ids:
        if _event.set():
            session.close()
            return
        
        sections = session.query(db.Section).filter(
            db.Section.parent_id.in_(ids)).order_by(db.Section.number).all()
        
        if sections:
            e.clear()
        
        parents = set()
        counter = {'value': len(sections)}
        
        if len(sections):
            for c in sections:
                parent = iters[c.parent_id]
                
                if c.id in search_active:
                    enable_search = search_active[c.id]
                else:
                    enable_search = False
                
                Gdk.threads_add_idle(GLib.PRIORITY_LOW, call_count,
                    append_to_treestore, counter, e,
                    treestore, parent,
                    [c.id, c.number, c.name, label_template.format(c),
                        enable_search])
                
                parents.add(parent)
            
            e.wait()
        
        for c in parents:
            if c is None:
                for d in treestore:
                    iters[d[0]] = d.iter
            else:
                for d in treestore[c].iterchildren():
                    iters[d[0]] = d.iter
        
        ids = [c.id for c in sections]
    
    session.close()
    
    old_search_active = {c: search_active[c] for c in search_active
        if search_active[c]}
    search_active = get_treestore_column(treestore, 4)
    new_search_active = {c: search_active[c] for c in search_active
        if search_active[c]}
    if old_search_active != new_search_active:
        populate_books_flowbox()

@giqra_thread.threadfun
def populate_libraries_treestore(_event):
    session = util.get_scoped_session()
    
    treestore = ui['giqra'].get_object('libraries_treestore')
    
    search_active = {c[0]: c[2] for c in treestore}
    
    gtk_call_wait(clear_store, treestore)
    
    libraries = session.query(db.Library).order_by(db.Library.name)
    
    if 0 in search_active:
        enable_search = search_active[0]
    else:
        enable_search = False
    
    Gdk.threads_add_idle(GLib.PRIORITY_LOW, append_to_treestore,
        treestore, None, ['0', '-----', enable_search])
    
    for c in libraries:
        if c.id in search_active:
            enable_search = search_active[c.id]
        else:
            enable_search = False
        
        Gdk.threads_add_idle(GLib.PRIORITY_LOW, append_to_treestore,
            treestore, None, [str(c.id), c.name, enable_search])
    
    session.close()

@giqra_thread.threadfun
def populate_authors_search_treestore(_event):
    LIMIT = 5
    adj = ui['giqra'].get_object(
        'authors_treeview').get_parent().get_vadjustment()
    search_text = ui['giqra'].get_object('author_search_entry').get_text()
    
    treestore = ui['giqra'].get_object('authors_search_treestore')
    gtk_call_wait(clear_store, treestore)
    
    session = util.get_scoped_session()
    
    q = session.query(db.Author).order_by(db.Author.name)
    
    if search_text:
        words = search_text.split()
        
        for c in words:
            q = q.filter(db.Author.name.contains(c))
    
    e = threading.Event()
    counter = {'value': 0}
    
    offset = len(treestore)
    authors = partial_query(q, offset, LIMIT)
    while authors:
        counter['value'] = len(authors)
        for c in authors:
            Gdk.threads_add_idle(GLib.PRIORITY_LOW, call_count,
                append_to_treestore, counter, e,
                treestore, None, [c.id, c.name])
        
        if adj.get_value() <= adj.get_upper() - 2 * adj.get_page_size():
            t = 0.1
        else:
            t = 0.01
        
        e.wait()
        
        if _event.wait(t):
            break
        
        offset = len(treestore)
        authors = partial_query(q, offset, LIMIT)
    
    session.close()
    
@giqra_thread.threadfun
def populate_publishers_search_treestore(_event):
    LIMIT = 5
    adj = ui['giqra'].get_object(
        'publishers_treeview').get_parent().get_vadjustment()
    search_text = ui['giqra'].get_object('publisher_search_entry').get_text()
    
    treestore = ui['giqra'].get_object('publishers_search_treestore')
    gtk_call_wait(clear_store, treestore)
    
    session = util.get_scoped_session()
    
    q = session.query(db.Publisher).order_by(db.Publisher.name)
    
    if search_text:
        words = search_text.split()
        
        for c in words:
            q = q.filter(db.Publisher.name.contains(c))
    
    e = threading.Event()
    counter = {'value': 0}
    
    offset = len(treestore)
    publishers = partial_query(q, offset, LIMIT)
    while publishers:
        counter['value'] = 0
        for c in publishers:
            Gdk.threads_add_idle(GLib.PRIORITY_LOW, call_count,
                append_to_treestore, counter, e,
                treestore, None, [c.id, c.name])
        
        if adj.get_value() <= adj.get_upper() - 2 * adj.get_page_size():
            t = 0.1
        else:
            t = 0.01
        
        e.wait()
        
        if _event.wait(t):
            break
        
        offset = len(treestore)
        publishers = partial_query(q, offset, LIMIT)
    
    session.close()

@giqra_thread.threadfun
def populate_borrows_search_liststore(_event):
    LIMIT = 5
    adj = ui['giqra'].get_object(
        'borrows_treeview').get_parent().get_vadjustment()
    search_text = ui['giqra'].get_object('borrow_search_entry').get_text()
    
    treestore = ui['giqra'].get_object('borrows_search_liststore')
    gtk_call_wait(clear_store, treestore)
    
    session = util.get_scoped_session()
    
    q = session.query(db.Borrow)
    
    if search_text:
        number = [int(c) for c in search_text.split('-')]
        book_ids = util.get_books(
            session, *number, columns=[db.Book.id]).subquery()
        q = q.filter(db.Borrow.book_id.in_(book_ids))
    
    q.order_by(db.Borrow.date)
    
    e = threading.Event()
    counter = {'value': 0}
    
    offset = len(treestore)
    borrows = partial_query(q, offset, LIMIT)
    while borrows:
        counter['value'] = len(borrows)
        for c in borrows:
            if c.return_date is not None:
                background = 'light green'
            else:
                background = None
            Gdk.threads_add_idle(GLib.PRIORITY_LOW, call_count,
                    append_to_treestore, counter, e,
                    treestore, None, [
                        c.id, c.book.unpadded_full_number, c.book.library_name,
                        c.borrower, c.contact, c.date_str,
                        c.return_date_str, background
                    ]
                )
        
        if adj.get_value() <= adj.get_upper() - 2 * adj.get_page_size():
            t = 0.1
        else:
            t = 0.01
        
        e.wait()
        
        if _event.wait(t):
            break
        
        offset = len(treestore)
        borrows = partial_query(q, offset, LIMIT)
    
    session.close()

@giqra_thread.threadfun
def populate_parents_label(number, label, _event):
    try:
        if type(label) is str:
            label = ui['giqra'].get_object(label)
        
        session = util.get_scoped_session()
        number = [int(c) for c in number.split('-')[:-1]]
        sections = []
        
        section = util.get_root_section(session)
        for c in number:
            section = session.query(db.Section).filter_by(
                parent=section, number=c).one()
            sections.append(section.name)
        
        label.set_label('-'.join(sections))
    except Exception as e:
        label.set_label('')
    finally:
        session.close()

@giqra_thread.threadfun
def populate_books_flowbox(_event):
    LIMIT = 5
    adj = ui['giqra'].get_object('books_flowbox').get_parent().get_vadjustment()
    
    gtk_call_wait(clear_store, books_search_liststore)
    
    search_text = ui['giqra'].get_object('book_search_entry').get_text()
    
    treestore = ui['giqra'].get_object('sections_treestore')
    sections = get_treestore_column(treestore, 4)
    sections = [c for c in sections if sections[c]]
    
    treestore = ui['giqra'].get_object('libraries_treestore')
    libraries = get_treestore_column(treestore, 2)
    libraries = [c for c in libraries if libraries[c]]
    try:
        idx = libraries.index(0)
        libraries[idx] = None
    except ValueError:
        pass
    
    session = util.get_scoped_session()
    q = session.query(db.Book)
    if search_text:
        words = search_text.split()
        tags_sq = session.query(db.Tag.book_id)
        author_sq = session.query(
                db.BookAuthor.book_id
            ).join(
                db.Author
            )
        publisher_sq = session.query(db.Publisher.id)
        for c in words:
            tags_cond = tags_sq.filter(
                    db.Tag.text.contains(c)
                ).group_by(
                    db.Tag.book_id
                ).subquery()
            authors_cond = author_sq.filter(
                    db.Author.name.contains(c)
                ).group_by(
                    db.BookAuthor.book_id
                ).subquery()
            publishers_cond = publisher_sq.filter(
                    db.Publisher.name.contains(c)
                ).subquery()
            
            title_cond = db.Book.title.contains(c)
            tags_cond = db.Book.id.in_(tags_cond)
            authors_cond = db.Book.id.in_(authors_cond)
            publishers_cond = db.Book.publisher_id.in_(publishers_cond)
            q = q.filter(sqlalchemy.or_(
                    title_cond,
                    tags_cond,
                    authors_cond,
                    publishers_cond
                ))
    
    if sections:
        q = q.filter(db.Book.section_id.in_(sections))
    
    if libraries:
        q = q.filter(db.Book.library_id.in_(libraries))
    
    q = q.group_by(db.Book.section_id, db.Book.number)
    
    offset = books_search_liststore.get_n_items()
    books = partial_query(q, offset, LIMIT)
    while books:
        for c in books:
            obj = GDict()
            for attr_name in ('id', 'title', 'unpadded_full_number',
                    'authors_names', 'publisher_name', 'publication_year_str',
                    'language', 'tags_text'):
                obj[attr_name] = getattr(c, attr_name)
            Gdk.threads_add_idle(GLib.PRIORITY_LOW,
                books_search_liststore.append,
                obj
            )
        
        if adj.get_value() <= adj.get_upper() - 2 * adj.get_page_size():
            t = 0.1
        else:
            t = 0.01
        
        if _event.wait(t):
            break
        
        offset = books_search_liststore.get_n_items()
        books = partial_query(q, offset, LIMIT)
    
    session.close()

def partial_query(q, offset, limit):
    results = q.offset(offset).limit(limit).all()
    util.get_scoped_session().rollback()
    return results

def create_book_widget(item):
    LABEL_TEMPLATE = '<span font="10">{[title]}</span>'
    TOOLTIP_TEMPLATE = (
        _('number:') + ' {0[unpadded_full_number]}\n' +
        _('title:') + ' {0[title]}\n' +
        _('authors:') + ' {0[authors_names]}\n' +
        _('publisher:') + ' {0[publisher_name]} {0[publication_year_str]}\n' +
        _('language:') + ' {0[language]}\n' +
        _('tags:') + ' {0[tags_text]}'
    )
    
    label = Gtk.Label(item['title'])
    
    thumb = Gtk.Image.new_from_pixbuf(get_thumb(item['id']))
        
    label = Gtk.Label()
    label.set_halign(Gtk.Align.CENTER)
    label.set_max_width_chars(30)
    label.set_ellipsize(Pango.EllipsizeMode.END)
    label.set_markup(LABEL_TEMPLATE.format(item))
    
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box.pack_start(thumb, True, True, 0)
    box.pack_start(label, False, False, 0)
    
    box.set_tooltip_text(TOOLTIP_TEMPLATE.format(item))
    box.book_id = item['id']
    box.show_all()
    
    return box

#book edit
def edit_book(id_=None):
    session = util.get_scoped_session()
    model = ui['giqra'].get_object('book_edit_language')
    model.remove_all()
    for c in session.query(db.Book.language.distinct()):
        model.append_text(c[0])
    
    entry = ui['giqra'].get_object('book_edit_publishers_search_entry')
    populate_book_edit_publishers_search_tree(entry.get_text())
    entry = ui['giqra'].get_object('book_edit_authors_search_entry')
    populate_book_edit_authors_search_tree(entry.get_text())
    
    ui['giqra'].get_object('edit_book_page').id = id_
    
    combo = ui['giqra'].get_object('copy_combobox')
    combo.remove_all()
    
    if id_ is None:
        empty_edit_book()
        combo.hide()
        ui['giqra'].get_object('copies_label').hide()
    else:
        book = session.query(
            db.Book.number, db.Book.section_id).filter_by(id=id_).one()
        copies = session.query(db.Book.id).filter_by(
            number=book[0], section_id=book[1])
        
        if copies.count() > 1:
            for idx, c in enumerate(copies):
                combo.append(str(c[0]), str(idx+1))
            
            combo.set_active_id(str(id_))
            combo.show_all()
            ui['giqra'].get_object('copies_label').show_all()
        else:
            combo.hide()
            ui['giqra'].get_object('copies_label').hide()
            populate_edit_book(id_)
    
    ui['giqra'].get_object('edit_stack').set_visible_child_name(
        'book_edit_page')
    ui['giqra'].get_object('toplevel_stack').set_visible_child_name('edit_page')

def empty_edit_book():
    ui['giqra'].get_object('book_edit_thumb').path = None
    ui['giqra'].get_object('book_edit_thumb_image').set_from_pixbuf(None)
    empty_textboxes('book_edit_number',
        'book_edit_title', 'book_edit_tags')
    ui['giqra'].get_object('book_edit_is_electronic').set_active(False)
    ui['giqra'].get_object('electronic_files_liststore').clear()
    
    label = ui['giqra'].get_object('book_edit_publisher')
    label.id = None
    label.set_label('-----')
    
    ui['giqra'].get_object('book_edit_publication_year').set_value(
        datetime.date.today().year)
    
    ui['giqra'].get_object('book_edit_language').get_child().set_text('')
    
    try:
        ui['giqra'].get_object('book_edit_library').set_active(1)
    except Exception:
        ui['giqra'].get_object('book_edit_library').set_active(0)
    
    ui['giqra'].get_object('book_edit_authors_liststore').clear()
    ui['giqra'].get_object('book_edit_borrows_liststore').clear()

def populate_edit_book(id_):
    book = util.get_scoped_session().query(db.Book).get(id_)
    
    ui['giqra'].get_object('book_edit_thumb').path = util.get_thumbs(id_)[0]
    ui['giqra'].get_object('book_edit_thumb_image').set_from_pixbuf(
        get_thumb(id_, False))
    ui['giqra'].get_object('book_edit_number').set_text(
        book.unpadded_full_number)
    ui['giqra'].get_object('book_edit_title').set_text(book.title)
    ui['giqra'].get_object('book_edit_tags').set_text(book.tags_text)
    ui['giqra'].get_object('book_edit_is_electronic').set_active(
        book.is_electronic)
    
    model = ui['giqra'].get_object('electronic_files_liststore')
    model.clear()
    for c in util.get_electronic_files(book.id):
        model.append([str(c), c.name])
    
    label = ui['giqra'].get_object('book_edit_publisher')
    if book.publisher_id is not None:
        label.id = book.publisher_id
        label.set_label(book.publisher.name)
    else:
        label.id = None
        label.set_label('-----')
    
    spin = ui['giqra'].get_object('book_edit_publication_year')
    if book.publication_year is not None:
        spin.set_value(book.publication_year)
    else:
        spin.set_value(0)
    
    ui['giqra'].get_object('book_edit_language').get_child().set_text(
        book.language)
    
    ui['giqra'].get_object('book_edit_library').set_active_id(
        str(book.library_id))
    
    model = ui['giqra'].get_object('book_edit_authors_liststore')
    model.clear()
    
    for c in book.authors:
        model.append([c.id, c.name])
    
    model = ui['giqra'].get_object('book_edit_borrows_liststore')
    model.clear()
    session = util.get_scoped_session()
    q = session.query(db.Borrow).filter(db.Borrow.book_id == book.id).limit(10)
    for c in q:
        model.append(
                [
                    c.id,
                    c.borrower,
                    c.contact,
                    c.date_str,
                    c.return_date_str
                ]
            )

def populate_book_edit_publishers_search_tree(word=''):
    model = ui['giqra'].get_object('book_edit_publishers_search_liststore')
    model.clear()
    model.append([None, '-----'])
    q = util.get_scoped_session().query(db.Publisher)
    if word:
        q = q.filter(db.Publisher.name.contains(word))
    for c in q.order_by(db.Publisher.name).limit(5):
        model.append([c.id, c.name])
    
def populate_book_edit_authors_search_tree(word=''):
    model = ui['giqra'].get_object('book_edit_authors_search_liststore')
    model.clear()
    q = util.get_scoped_session().query(db.Author)
    if word:
        q = q.filter(
            db.Author.name.contains(word))
    for c in q.order_by(db.Author.name).limit(5):
        model.append([c.id, c.name])

#section edit
def edit_section(id_=None):
    ui['giqra'].get_object('edit_section_page').id = id_
    if id_ is None:
        empty_edit_section()
    else:
        populate_edit_section(id_)
    
    ui['giqra'].get_object('edit_stack').set_visible_child_name(
        'section_edit_page')
    ui['giqra'].get_object('toplevel_stack').set_visible_child_name('edit_page')

def empty_edit_section():
    empty_textboxes('section_edit_number',
        'section_edit_name', 'section_edit_abbreviation')
    section_edit_populate_books()

def populate_edit_section(id_):
    section = util.get_scoped_session().query(db.Section).get(id_)
    ui['giqra'].get_object('section_edit_number').set_text(
        section.unpadded_full_number)
    ui['giqra'].get_object('section_edit_name').set_text(section.name)
    ui['giqra'].get_object('section_edit_abbreviation').set_text(
        section.abbreviation)
    section_edit_populate_books()

def section_edit_populate_books():
    id_ = ui['giqra'].get_object('edit_section_page').id
    model = ui['giqra'].get_object('edit_books_liststore')
    model.clear()
    if id_ is not None:
        label_text = '\n'.join(
                [
                    '<b>{0.title}</b>',
                    '{0.authors_names}',
                    '{0.publisher_name}',
                    '{0.library_name}',
                    '{0.unpadded_full_number}'
                ]
            )
        
        session = util.get_scoped_session()
        q = session.query(db.Book).filter_by(section_id=id_).group_by(
            db.Book.number)
        
        count = q.count()
        samples = min(count, 10)
        books = [q[c] for c in random.sample(range(count), samples)]
        for c in books:
            model.append([c.id, get_thumb(c.id, False), label_text.format(c)])

#author edit
def edit_author(id_=None):
    ui['giqra'].get_object('edit_author_page').id = id_
    if id_ is None:
        empty_edit_author()
    else:
        populate_edit_author(id_)
    
    ui['giqra'].get_object('edit_stack').set_visible_child_name(
        'author_edit_page')
    ui['giqra'].get_object('toplevel_stack').set_visible_child_name('edit_page')

def empty_edit_author():
    empty_textboxes('author_edit_name')
    ui['giqra'].get_object('author_edit_about').get_buffer().set_text('')
    author_edit_populate_books()

def populate_edit_author(id_):
    author = util.get_scoped_session().query(db.Author).get(id_)
    ui['giqra'].get_object('author_edit_name').set_text(author.name)
    ui['giqra'].get_object(
        'author_edit_about').get_buffer().set_text(author.about)
    author_edit_populate_books()

def author_edit_populate_books():
    id_ = ui['giqra'].get_object('edit_author_page').id
    model = ui['giqra'].get_object('edit_books_liststore')
    model.clear()
    if id_ is not None:
        label_text = '\n'.join(
                [
                    '<b>{0.title}</b>',
                    '{0.authors_names}',
                    '{0.publisher_name}',
                    '{0.library_name}',
                    '{0.unpadded_full_number}'
                ]
            )
        
        session = util.get_scoped_session()
        sq = session.query(db.BookAuthor.book_id).filter_by(
            author_id=id_).subquery()
        q = session.query(db.Book).join(db.BookAuthor).filter(
            db.Book.id.in_(sq)).group_by(db.Book.section_id, db.Book.number)
        
        count = q.count()
        samples = min(count, 10)
        books = [q[c] for c in random.sample(range(count), samples)]
        for c in books:
            model.append([c.id, get_thumb(c.id, False), label_text.format(c)])

#publisher edit
def edit_publisher(id_=None):
    ui['giqra'].get_object('edit_publisher_page').id = id_
    if id_ is None:
        empty_edit_publisher()
    else:
        populate_edit_publisher(id_)
    
    ui['giqra'].get_object('edit_stack').set_visible_child_name(
        'publisher_edit_page')
    ui['giqra'].get_object('toplevel_stack').set_visible_child_name('edit_page')

def empty_edit_publisher():
    empty_textboxes('publisher_edit_name')
    ui['giqra'].get_object('publisher_edit_about').get_buffer().set_text('')
    publisher_edit_populate_books()

def populate_edit_publisher(id_):
    publisher = util.get_scoped_session().query(db.Publisher).get(id_)
    ui['giqra'].get_object('publisher_edit_name').set_text(publisher.name)
    ui['giqra'].get_object(
        'publisher_edit_about').get_buffer().set_text(publisher.about)
    publisher_edit_populate_books()

def publisher_edit_populate_books():
    id_ = ui['giqra'].get_object('edit_publisher_page').id
    model = ui['giqra'].get_object('edit_books_liststore')
    model.clear()
    if id_ is not None:
        label_text = '\n'.join(
                [
                    '<b>{0.title}</b>',
                    '{0.authors_names}',
                    '{0.publisher_name}',
                    '{0.library_name}',
                    '{0.unpadded_full_number}'
                ]
            )
        
        session = util.get_scoped_session()
        q = session.query(db.Book).filter_by(publisher_id=id_).group_by(
            db.Book.section_id, db.Book.number)
        
        count = q.count()
        samples = min(count, 10)
        books = [q[c] for c in random.sample(range(count), samples)]
        for c in books:
            model.append([c.id, get_thumb(c.id, False), label_text.format(c)])

#library edit
def edit_library(id_=None):
    ui['giqra'].get_object('edit_library_page').id = id_
    if id_ is None:
        empty_edit_library()
    else:
        populate_edit_library(id_)
    
    ui['giqra'].get_object('edit_stack').set_visible_child_name(
        'library_edit_page')
    ui['giqra'].get_object('toplevel_stack').set_visible_child_name('edit_page')

def empty_edit_library():
    empty_textboxes('library_edit_name')
    publisher_edit_populate_books()

def populate_edit_library(id_):
    library = util.get_scoped_session().query(db.Library).get(id_)
    ui['giqra'].get_object('library_edit_name').set_text(library.name)
    library_edit_populate_books()

def library_edit_populate_books():
    id_ = ui['giqra'].get_object('edit_library_page').id
    model = ui['giqra'].get_object('edit_books_liststore')
    model.clear()
    if id_ is not None:
        label_text = '\n'.join(
                [
                    '<b>{0.title}</b>',
                    '{0.authors_names}',
                    '{0.publisher_name}',
                    '{0.library_name}',
                    '{0.unpadded_full_number}'
                ]
            )
        
        session = util.get_scoped_session()
        q = session.query(db.Book).filter_by(
            library_id=id_).group_by(
                db.Book.section_id, db.Book.number)
        
        count = q.count()
        samples = min(count, 10)
        books = [q[c] for c in random.sample(range(count), samples)]
        for c in books:
            model.append([c.id, get_thumb(c.id, False), label_text.format(c)])

def edit_borrow(id_=None):
    ui['giqra'].get_object('edit_borrow_page').id = id_
    if id_ is None:
        empty_edit_borrow()
    else:
        populate_edit_borrow(id_)
    
    ui['giqra'].get_object('edit_stack').set_visible_child_name(
        'borrow_edit_page')
    ui['giqra'].get_object('toplevel_stack').set_visible_child_name('edit_page')

def empty_edit_borrow():
    empty_textboxes('borrow_edit_number', 'borrow_edit_borrower',
        'borrow_edit_contact')
    
    today = datetime.date.today()
    calendar = ui['giqra'].get_object('borrow_edit_calendar')
    calendar.select_month(today.month, today.year)
    calendar.select_day(today.day)
    
    calendar = ui['giqra'].get_object('borrow_edit_return_calendar')
    calendar.select_month(today.month, today.year)
    calendar.select_day(today.day)
    ui['giqra'].get_object('borrow_edit_return_date').set_text('')

def populate_edit_borrow(id_):
    borrow = util.get_scoped_session().query(db.Borrow).get(id_)
    ui['giqra'].get_object('borrow_edit_number').set_text(
        borrow.book.unpadded_full_number)
    ui['giqra'].get_object('borrow_edit_borrower').set_text(borrow.borrower)
    ui['giqra'].get_object('borrow_edit_contact').set_text(borrow.contact)
    calendar = ui['giqra'].get_object('borrow_edit_calendar')
    calendar.select_month(borrow.date.month, borrow.date.year)
    calendar.select_day(borrow.date.day)
    
    if borrow.return_date is not None:
        calendar = ui['giqra'].get_object('borrow_edit_return_calendar')
        calendar.select_month(borrow.return_date.month, borrow.return_date.year)
        calendar.select_day(borrow.return_date.day)
    else:
        today = datetime.date.today()
        calendar = ui['giqra'].get_object('borrow_edit_return_calendar')
        calendar.select_month(today.month, today.year)
        calendar.select_day(today.day)
        ui['giqra'].get_object('borrow_edit_return_date').set_text('')
    

def empty_textboxes(*args):
    for c in args:
        if type(c) is str:
            c = ui['giqra'].get_object(c)
        c.set_text('')

def initialize_gui():
    global ui, books_search_liststore, plugins_liststore
    
    ui_path = str(configdirs.path('res/glade/main.glade'))
    ui = Gtk.Builder()
    
    ui.set_translation_domain('giqra')
    ui.add_from_file(ui_path)
    ui = {'giqra': ui}
    
    trans_ui(ui, trans_dir)
    
    plugins_liststore = Gio.ListStore.new(GDict)
    ui['giqra'].get_object('plugins_listbox').bind_model(
        plugins_liststore, create_plugin_widget)
    
    books_search_liststore = Gio.ListStore.new(GDict)
    ui['giqra'].get_object('books_flowbox').bind_model(
        books_search_liststore, create_book_widget)
    
    ui['giqra'].get_object('libraries_model_filter').set_visible_func(
        lambda model, idx, data: model[idx][0] != '0')
    
    ui['giqra'].connect_signals(Handler)
    ui['giqra'].get_object('main_win').show_all()
    
    populate_plugins()
    populate_books_flowbox()
    populate_sections_treestore()
    populate_libraries_treestore()
    populate_authors_search_treestore()
    populate_publishers_search_treestore()
    populate_borrows_search_liststore()
    
class Handler:
    @staticmethod
    def on_main_win_destroy(*args, **kwargs):
        Gtk.main_quit()
    
    @staticmethod
    def on_books_flowbox_parent_set(flowbox):
        parent = flowbox.get_parent()
        if parent is not None:
            if type(parent) is not Gtk.ScrolledWindow:
                parent = parent.get_parent()
    
    #books page
    @staticmethod
    def on_books_sections_search_active_toggled(renderer, path):
        treestore = ui['giqra'].get_object('sections_treestore')
        treestore[path][4] = not treestore[path][4]
        populate_books_flowbox()
    
    @staticmethod
    def on_books_sections_treeview_row_activated(tree, path, column):
        model = tree.get_model()
        rows = [model[path]]
        
        new_rows = rows
        while new_rows:
            children = []
            for c in new_rows:
                children.extend([child for child in c.iterchildren()])
            
            rows.extend(children)
            new_rows = children
        
        for c in reversed(rows):
            c[4] = not rows[0][4]
        
        populate_books_flowbox()
    
    @staticmethod
    def books_sections_unfilter(button):
        model = ui['giqra'].get_object('sections_treestore')
        
        rows = []
        row = model.iter_children(None)
        while row is not None:
            rows.append(model[row])
            row = model.iter_next(row)
        
        new_rows = rows
        while new_rows:
            children = []
            for c in new_rows:
                children.extend([child for child in c.iterchildren()])
            
            rows.extend(children)
            new_rows = children
        
        for c in rows:
            c[4] = False
        
        populate_books_flowbox()
    
    @staticmethod
    def books_libraries_unfilter(button):
        model = ui['giqra'].get_object('libraries_treestore')
        
        rows = []
        row = model.iter_children(None)
        while row is not None:
            rows.append(model[row])
            row = model.iter_next(row)
        
        new_rows = rows
        while new_rows:
            children = []
            for c in new_rows:
                children.extend([child for child in c.iterchildren()])
            
            rows.extend(children)
            new_rows = children
        
        for c in rows:
            c[2] = False
        
        populate_books_flowbox()
    
    @staticmethod
    def on_books_libraries_search_active_toggled(renderer, path):
        treestore = ui['giqra'].get_object('libraries_treestore')
        treestore[path][2] = not treestore[path][2]
        populate_books_flowbox()
    
    @staticmethod
    def on_book_search_entry_activate(*args):
        populate_books_flowbox()
        ui['giqra'].get_object('book_search_popover').popdown()
    
    #book edit
    @staticmethod
    def on_books_flowbox_child_activated(flowbox, child):
        id_ = child.get_child().book_id
        edit_book(id_)
    
    @staticmethod
    def on_add_book_button_clicked(button):
        edit_book()
    
    @staticmethod
    def on_copy_combobox_changed(combo):
        id_ = combo.get_active_id()
        if id_ is not None:
            id_ = int(id_)
            ui['giqra'].get_object('edit_book_page').id = id_
            populate_edit_book(id_)
    
    @staticmethod
    def on_book_edit_number_changed(entry):
        number = entry.get_text()
        populate_parents_label(number, 'book_edit_parents')
    
    @staticmethod
    def on_book_edit_is_electronic_toggled(checkbutton):
        ui['giqra'].get_object('electronic_files_box').set_visible(
            checkbutton.get_active())
    
    @staticmethod
    def on_remove_electronic_button_clicked(button):
        tree = ui['giqra'].get_object('book_edit_electronic_treeview')
        model, row = tree.get_selection().get_selected()
        if row is not None:
            del model[row]
    
    @staticmethod
    def on_add_electronic_button_clicked(button):
        dialog = ui['giqra'].get_object('open_dialog')
        response = dialog.run()
        
        dialog.hide()
        if response == Gtk.ResponseType.OK:
            fname = dialog.get_filename()
            f = pathlib.Path(fname)
            if f.exists():
                model = ui['giqra'].get_object('electronic_files_liststore')
                model.append([str(f), f.name])
    
    @staticmethod
    def on_book_edit_thumb_clicked(button):
        dialog = ui['giqra'].get_object('thumb_open_dialog')
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.OK:
            fname = dialog.get_filename()
            f = pathlib.Path(fname)
            if f.exists():
                button.path = fname
                thumb = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    str(f), 128, 128)
                ui['giqra'].get_object(
                    'book_edit_thumb_image').set_from_pixbuf(thumb)
        elif response == Gtk.ResponseType.REJECT:
            button.path = None
            ui['giqra'].get_object(
                'book_edit_thumb_image').set_from_pixbuf(None)
    
    @staticmethod
    def on_book_edit_authors_search_entry_search_changed(entry):
        populate_book_edit_authors_search_tree(entry.get_text())
    
    @staticmethod
    def on_book_edit_authors_tree_row_activated(tree, path, column=0):
        ui['giqra'].get_object('book_edit_authors_popover').popdown()
        model, row = tree.get_selection().get_selected()
        value = list(model[row])
        authors_store = ui['giqra'].get_object('book_edit_authors_liststore')
        ids = [c[0] for c in authors_store]
        if value[0] not in ids:
            authors_store.append(value)
    
    @staticmethod
    def on_book_edit_author_remove_button_clicked(button):
        tree = ui['giqra'].get_object('book_edit_authors_treeview')
        model, row = tree.get_selection().get_selected()
        if row is not None:
            del model[row]
    
    @staticmethod
    def on_book_edit_publishers_search_entry_search_changed(entry):
        populate_book_edit_publishers_search_tree(entry.get_text())
    
    @staticmethod
    def on_book_edit_publishers_tree_row_activated(tree, path, column=0):
        ui['giqra'].get_object('book_edit_publishers_popover').popdown()
        model, row = tree.get_selection().get_selected()
        
        label = ui['giqra'].get_object('book_edit_publisher')
        label.set_label(model[row][1])
        label.id = model[row][0]
    
    @staticmethod
    def on_book_edit_apply_button_clicked(button):
        id_ = ui['giqra'].get_object('edit_book_page').id
        number = ui['giqra'].get_object('book_edit_number').get_text()
        number = [int(c) for c in number.split('-')]
        
        session = util.get_scoped_session()
        parent = util.get_root_section(session)
        for c in number[:-1]:
            parent = session.query(db.Section).filter_by(
                parent=parent, number=c).one()
        
        library_model = ui['giqra'].get_object('book_edit_library').get_model()
        library_iter = ui['giqra'].get_object(
            'book_edit_library').get_active_iter()
        library_id = library_model[library_iter][0]
        
        title = ui['giqra'].get_object('book_edit_title').get_text()
        
        is_electronic = ui['giqra'].get_object(
            'book_edit_is_electronic').get_active()
        model = ui['giqra'].get_object('electronic_files_liststore')
        ecopies = [pathlib.Path(c[0]) for c in model]
        ecopies = set(ecopies)
        
        publisher_id = ui['giqra'].get_object('book_edit_publisher').id
        publication_year = ui['giqra'].get_object(
            'book_edit_publication_year').get_value()
        
        language = ui['giqra'].get_object(
            'book_edit_language').get_active_text()
        
        authors_model = ui['giqra'].get_object('book_edit_authors_liststore')
        authors = [session.query(db.Author).get(c[0]) for c in authors_model]
        
        tags = ui['giqra'].get_object('book_edit_tags').get_text().split()
        tags = set(tags)
        
        try:
            if id_ is None:
                book = db.Book()
                session.add(book)
            else:
                book = session.query(db.Book).get(id_)
            
            book.number = number[-1]
            book.section = parent
            book.library_id = library_id
            book.title = title
            book.is_electronic = is_electronic
            book.publisher_id = publisher_id
            book.publication_year = publication_year
            book.language = language
            book.authors = authors
            
            old_tags = [c.text for c in book.tags]
            kept_tags = [c for c in book.tags if c.text in tags]
            new_tags = [db.Tag(text=c) for c in tags if c not in old_tags]
            
            book.tags = kept_tags + new_tags
            
            session.commit()
            thumb = ui['giqra'].get_object('book_edit_thumb').path
            
            if thumb is not None:
                util.set_thumb(book.id, thumb)
            else:
                util.delete_thumb(book.id)
            
            populate_books_flowbox()
            
            if is_electronic:
                existing = util.get_electronic_files(book.id)
                to_delete = [c for c in existing if c not in ecopies]
                to_add = [c for c in ecopies if c not in existing]
                for c in to_delete:
                    util.delete_electronic_file(book.id, c.suffix)
                for c in to_add:
                    util.add_electronic_file(book.id, c)
            
            stack = ui['giqra'].get_object('toplevel_stack')
            stack.set_visible_child_name('main_page')
            
        except Exception as e:
            print(repr(e))
            session.rollback()
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
    
    @staticmethod
    def on_book_edit_delete_button_clicked(button):
        dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'), 0,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _('Are you sure you want to delete?'))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            id_ = ui['giqra'].get_object('edit_book_page').id
            if id_ is not None:
                session = util.get_scoped_session()
                book = session.query(db.Book).get(id_)
                session.delete(book)
                try:
                    session.commit()
                    populate_books_flowbox()
                    stack = ui['giqra'].get_object('toplevel_stack')
                    stack.set_visible_child_name('main_page')
                except Exception as e:
                    print(repr(e))
                    session.rollback()
                    dialog = Gtk.MessageDialog(
                        ui['giqra'].get_object('main_win'),
                        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                        _('An error occurred!'))
                    dialog.format_secondary_text(type(e).__name__)
                    dialog.run()
                    dialog.destroy()
            else:
                stack = ui['giqra'].get_object('toplevel_stack')
                stack.set_visible_child_name('main_page')
    
    @staticmethod
    def on_book_edit_duplicate_clicked(button):
        ui['giqra'].get_object('edit_book_page').id = None
        ui['giqra'].get_object('copy_combobox').hide()
        ui['giqra'].get_object('copies_label').hide()
    
    #sections page
    @staticmethod
    def on_sections_treeview_row_activated(tree, path, column):
        id_ = tree.get_model()[path][0]
        edit_section(id_)
    
    @staticmethod
    def on_add_section_button_clicked(button):
        edit_section()
    
    #edit section
    @staticmethod
    def entry_check_empty(entry):
        if entry.get_text() and entry.get_icon_name(
                Gtk.EntryIconPosition.SECONDARY) is not None:
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
        elif not entry.get_text() and entry.get_icon_name(
                Gtk.EntryIconPosition.SECONDARY) is None:
            entry.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY, 'gtk-dialog-error')
    
    @staticmethod
    def on_section_edit_number_changed(entry):
        number = entry.get_text()
        populate_parents_label(number, 'section_edit_parents')
    
    @staticmethod
    def on_section_edit_delete_button_clicked(button):
        dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'), 0,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _('Are you sure you want to delete?'))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            id_ = ui['giqra'].get_object('edit_section_page').id
            if id_ is not None:
                session = util.get_scoped_session()
                section = session.query(db.Section).get(id_)
                session.delete(section)
                try:
                    session.commit()
                    populate_sections_treestore()
                    stack = ui['giqra'].get_object('toplevel_stack')
                    stack.set_visible_child_name('main_page')
                except Exception as e:
                    print(repr(e))
                    session.rollback()
                    dialog = Gtk.MessageDialog(
                        ui['giqra'].get_object('main_win'),
                        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                        _('An error occurred!'))
                    dialog.format_secondary_text(type(e).__name__)
                    dialog.run()
                    dialog.destroy()
            else:
                stack = ui['giqra'].get_object('toplevel_stack')
                stack.set_visible_child_name('main_page')
    
    @staticmethod
    def on_section_edit_apply_button_clicked(button):
        id_ = ui['giqra'].get_object('edit_section_page').id
        number = ui['giqra'].get_object('section_edit_number').get_text()
        name = ui['giqra'].get_object('section_edit_name').get_text()
        abbr = ui['giqra'].get_object('section_edit_abbreviation').get_text()
        
        session = util.get_scoped_session()
        try:
            number = [int(c) for c in number.split('-')]
            parent = util.get_root_section(session)
            for c in number[:-1]:
                parent = session.query(db.Section).filter_by(
                    parent=parent, number=c).one()
            
            if id_ is None:
                section = db.Section()
                session.add(section)
            else:
                section = session.query(db.Section).get(id_)
            
            section.parent = parent
            section.number = number[-1]
            section.name = name
            section.abbreviation = abbr
            
            session.commit()
            populate_sections_treestore()
            stack = ui['giqra'].get_object('toplevel_stack')
            stack.set_visible_child_name('main_page')
        except Exception as e:
            print(repr(e))
            session.rollback()
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
    
    #authors page
    @staticmethod
    def on_author_search_entry_activate(*args):
        populate_authors_search_treestore()
        ui['giqra'].get_object('author_search_popover').popdown()
    
    #authors edit
    @staticmethod
    def on_authors_treeview_row_activated(tree, path, column):
        id_ = tree.get_model()[path][0]
        edit_author(id_)
    
    @staticmethod
    def on_add_author_button_clicked(button):
        edit_author()
    
    @staticmethod
    def on_author_edit_delete_button_clicked(button):
        dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'), 0,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _('Are you sure you want to delete?'))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            id_ = ui['giqra'].get_object('edit_author_page').id
            if id_ is not None:
                session = util.get_scoped_session()
                author = session.query(db.Author).get(id_)
                session.delete(author)
                try:
                    session.commit()
                    ui['giqra'].get_object('authors_search_treestore').clear()
                    populate_authors_search_treestore()
                    stack = ui['giqra'].get_object('toplevel_stack')
                    stack.set_visible_child_name('main_page')
                except Exception as e:
                    print(repr(e))
                    session.rollback()
                    dialog = Gtk.MessageDialog(
                        ui['giqra'].get_object('main_win'),
                        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                        _('An error occurred!'))
                    dialog.format_secondary_text(type(e).__name__)
                    dialog.run()
                    dialog.destroy()
            else:
                stack = ui['giqra'].get_object('toplevel_stack')
                stack.set_visible_child_name('main_page')
    
    @staticmethod
    def on_author_edit_apply_button_clicked(button):
        id_ = ui['giqra'].get_object('edit_author_page').id
        name = ui['giqra'].get_object('author_edit_name').get_text()
        about = ui['giqra'].get_object('author_edit_about').get_buffer()
        about = about.get_text(about.get_start_iter(), about.get_end_iter(),
            False)
        
        session = util.get_scoped_session()
        try:
            if id_ is None:
                author = db.Author()
                session.add(author)
            else:
                author = session.query(db.Author).get(id_)
            
            author.name = name
            author.about = about
            
            session.commit()
            ui['giqra'].get_object('authors_search_treestore').clear()
            populate_authors_search_treestore()
            stack = ui['giqra'].get_object('toplevel_stack')
            stack.set_visible_child_name('main_page')
        except Exception as e:
            print(repr(e))
            session.rollback()
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
    
    #publishers page
    @staticmethod
    def _on_publishers_search_scrolled_window_edge_reached(
            widget, position):
        if position == Gtk.PositionType.BOTTOM:
            populate_publishers_search_treestore()
    
    @staticmethod
    def on_publisher_search_entry_activate(*args):
        ui['giqra'].get_object('publishers_search_treestore').clear()
        populate_publishers_search_treestore()
        ui['giqra'].get_object('publisher_search_popover').popdown()
    
    @staticmethod
    def _on_publishers_search_scrolled_window_edge_reached(
            widget, position):
        if position == Gtk.PositionType.BOTTOM:
            populate_publishers_search_treestore()
    
    #publishers edit
    @staticmethod
    def on_publishers_treeview_row_activated(tree, path, column):
        id_ = tree.get_model()[path][0]
        edit_publisher(id_)
    
    @staticmethod
    def on_add_publisher_button_clicked(button):
        edit_publisher()
    
    @staticmethod
    def on_publisher_edit_delete_button_clicked(button):
        dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'), 0,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _('Are you sure you want to delete?'))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            id_ = ui['giqra'].get_object('edit_publisher_page').id
            if id_ is not None:
                session = util.get_scoped_session()
                publisher = session.query(db.Publisher).get(id_)
                session.delete(publisher)
                try:
                    session.commit()
                    ui['giqra'].get_object(
                        'publishers_search_treestore').clear()
                    populate_publishers_search_treestore()
                    stack = ui['giqra'].get_object('toplevel_stack')
                    stack.set_visible_child_name('main_page')
                except Exception as e:
                    print(repr(e))
                    session.rollback()
                    dialog = Gtk.MessageDialog(
                        ui['giqra'].get_object('main_win'),
                        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                        _('An error occurred!'))
                    dialog.format_secondary_text(type(e).__name__)
                    dialog.run()
                    dialog.destroy()
            else:
                stack = ui['giqra'].get_object('toplevel_stack')
                stack.set_visible_child_name('main_page')
    
    @staticmethod
    def on_publisher_edit_apply_button_clicked(button):
        id_ = ui['giqra'].get_object('edit_publisher_page').id
        name = ui['giqra'].get_object('publisher_edit_name').get_text()
        about = ui['giqra'].get_object('publisher_edit_about').get_buffer()
        about = about.get_text(about.get_start_iter(), about.get_end_iter(),
            False)
        
        session = util.get_scoped_session()
        try:
            if id_ is None:
                publisher = db.Publisher()
                session.add(publisher)
            else:
                publisher = session.query(db.Publisher).get(id_)
            
            publisher.name = name
            publisher.about = about
            
            session.commit()
            ui['giqra'].get_object('publishers_search_treestore').clear()
            populate_publishers_search_treestore()
            stack = ui['giqra'].get_object('toplevel_stack')
            stack.set_visible_child_name('main_page')
        except Exception as e:
            print(repr(e))
            session.rollback()
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
    
    #library edit
    @staticmethod
    def on_libraries_treeview_row_activated(tree, path, column):
        id_ = tree.get_model()[path][0]
        edit_library(id_)
    
    @staticmethod
    def on_add_library_button_clicked(button):
        edit_library()
    
    @staticmethod
    def on_library_edit_delete_button_clicked(button):
        dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'), 0,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _('Are you sure you want to delete?'))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            id_ = ui['giqra'].get_object('edit_library_page').id
            if id_ is not None:
                session = util.get_scoped_session()
                library = session.query(db.Library).get(id_)
                session.delete(library)
                try:
                    session.commit()
                    populate_libraries_treestore()
                    stack = ui['giqra'].get_object('toplevel_stack')
                    stack.set_visible_child_name('main_page')
                except Exception as e:
                    print(repr(e))
                    session.rollback()
                    dialog = Gtk.MessageDialog(
                        ui['giqra'].get_object('main_win'),
                        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                        _('An error occurred!'))
                    dialog.format_secondary_text(type(e).__name__)
                    dialog.run()
                    dialog.destroy()
            else:
                stack = ui['giqra'].get_object('toplevel_stack')
                stack.set_visible_child_name('main_page')
    
    @staticmethod
    def on_library_edit_apply_button_clicked(button):
        id_ = ui['giqra'].get_object('edit_library_page').id
        name = ui['giqra'].get_object('library_edit_name').get_text()
        
        session = util.get_scoped_session()
        try:
            if id_ is None:
                library = db.Library()
                session.add(library)
            else:
                library = session.query(db.Library).get(id_)
            
            library.name = name
            
            session.commit()
            populate_libraries_treestore()
            stack = ui['giqra'].get_object('toplevel_stack')
            stack.set_visible_child_name('main_page')
        except Exception as e:
            print(repr(e))
            session.rollback()
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
    
    #borrows page
    @staticmethod
    def on_borrow_search_entry_activate(entry):
        populate_borrows_search_liststore()
        ui['giqra'].get_object('borrow_search_popover').popdown()
    
    #edit borrow
    @staticmethod
    def on_add_borrow_button_clicked(button):
        edit_borrow()
    
    def on_borrows_treeview_row_activated(tree, path, column):
        id_ = tree.get_model()[path][0]
        edit_borrow(id_)
    
    @staticmethod
    def on_return_borrow_button_clicked(button):
        model, row = ui['giqra'].get_object('borrows_selection').get_selected()
        if row is not None:
            id_ = model[row][0]
            session = util.get_scoped_session()
            borrow = session.query(db.Borrow).get(id_)
            borrow.return_()
            try:
                session.commit()
                populate_borrows_search_liststore()
            except Exception as e:
                print(repr(e))
                session.rollback()
                dialog = Gtk.MessageDialog(
                    ui['giqra'].get_object('main_win'),
                    0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                    _('An error occurred!'))
                dialog.format_secondary_text(type(e).__name__)
                dialog.run()
                dialog.destroy()
    
    @staticmethod
    def on_delete_borrow_button_clicked(button):
        model, row = ui['giqra'].get_object('borrows_selection').get_selected()
        if row is not None:
            id_ = model[row][0]
            session = util.get_scoped_session()
            borrow = session.query(db.Borrow).get(id_)
            session.delete(borrow)
            try:
                session.commit()
                populate_borrows_search_liststore()
            except Exception as e:
                print(repr(e))
                session.rollback()
                dialog = Gtk.MessageDialog(
                    ui['giqra'].get_object('main_win'),
                    0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                    _('An error occurred!'))
                dialog.format_secondary_text(type(e).__name__)
                dialog.run()
                dialog.destroy()
    
    @staticmethod
    def on_borrow_edit_number_changed(entry):
        number = entry.get_text()
        label = ui['giqra'].get_object('borrow_edit_book_name_label')
        try:
            number = [int(c) for c in number.split('-')]
            session = util.get_scoped_session()
            section = util.get_root_section(session)
            for c in number[:-1]:
                section = session.query(db.Section).filter_by(
                    parent=section, number=c).one()
            
            borrowed_sq = session.query(db.Borrow.book_id).filter_by(
                return_date=None).subquery()
            
            book = session.query(db.Book).filter(
                db.Book.section == section, db.Book.number == number[-1],
                    db.Book.is_electronic == False,
                        db.Book.id.notin_(borrowed_sq)).first()
            
            if book is not None:
                entry.id = book.id
                label.set_label(book.title)
            else:
                entry.id = None
                label.set_label('')
        except Exception as e:
            entry.id = None
            label.set_label('')
    
    @staticmethod
    def on_borrow_edit_calendar_day_selected(calendar):
        ui['giqra'].get_object('borrow_edit_date_popover').popdown()
        date = datetime.date(*calendar.get_date())
        date = '{:%Y-%m-%d}'.format(date)
        ui['giqra'].get_object('borrow_edit_date').set_text(date)
    
    @staticmethod
    def on_borrow_edit_return_calendar_day_selected(calendar):
        ui['giqra'].get_object('borrow_edit_return_date_popover').popdown()
        date = datetime.date(*calendar.get_date())
        date = '{:%Y-%m-%d}'.format(date)
        ui['giqra'].get_object('borrow_edit_return_date').set_text(date)
    
    @staticmethod
    def on_borrow_edit_return_delete_button_clicked(button):
        today = datetime.date.today()
        calendar = ui['giqra'].get_object('borrow_edit_return_calendar')
        calendar.select_month(today.month, today.year)
        calendar.select_day(today.day)
        ui['giqra'].get_object('borrow_edit_return_date').set_text('')
    
    @staticmethod
    def on_borrow_edit_delete_button_clicked(button):
        dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'), 0,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _('Are you sure you want to delete?'))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            id_ = ui['giqra'].get_object('edit_borrow_page').id
            if id_ is not None:
                session = util.get_scoped_session()
                borrow = session.query(db.Borrow).get(id_)
                session.delete(borrow)
                try:
                    session.commit()
                    populate_borrows_search_liststore()
                    stack = ui['giqra'].get_object('toplevel_stack')
                    stack.set_visible_child_name('main_page')
                except Exception as e:
                    print(repr(e))
                    session.rollback()
                    dialog = Gtk.MessageDialog(
                        ui['giqra'].get_object('main_win'),
                        0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                        _('An error occurred!'))
                    dialog.format_secondary_text(type(e).__name__)
                    dialog.run()
                    dialog.destroy()
            else:
                stack = ui['giqra'].get_object('toplevel_stack')
                stack.set_visible_child_name('main_page')
    
    @staticmethod
    def on_borrow_edit_apply_button_clicked(button):
        id_ = ui['giqra'].get_object('edit_borrow_page').id
        book_id = ui['giqra'].get_object('borrow_edit_number').id
        borrower = ui['giqra'].get_object('borrow_edit_borrower').get_text()
        contact = ui['giqra'].get_object('borrow_edit_contact').get_text()
        date = ui['giqra'].get_object('borrow_edit_date').get_text()
        return_date = ui['giqra'].get_object(
            'borrow_edit_return_date').get_text()
        
        session = util.get_scoped_session()
        try:
            if id_ is None:
                borrow = db.Borrow()
                session.add(borrow)
            else:
                borrow = session.query(db.Borrow).get(id_)
            

            borrow.book_id = book_id
            borrow.borrower = borrower
            borrow.contact = contact
            borrow.date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if return_date:
                borrow.return_date = datetime.datetime.strptime(
                    return_date, '%Y-%m-%d')
            else:
                borrow.return_date = None
            
            session.commit()
            populate_borrows_search_liststore()
            stack = ui['giqra'].get_object('toplevel_stack')
            stack.set_visible_child_name('main_page')
        except Exception as e:
            print(repr(e))
            session.rollback()
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
    
    #general
    @staticmethod
    def on_edit_back_button_clicked(button):
        ui['giqra'].get_object('toplevel_stack').set_visible_child_name(
            'main_page')
    
    @staticmethod
    def on_settings_button_clicked(button):
        builder = ui['giqra']
        
        lang = builder.get_object('language_config')
        if len(lang.get_model()) <= 0:
            langs = [c.name for c in configdirs.glob('res/translations/mo/*')
                if c.is_dir()]
            for c in langs:
                lang.append(c, _(c))
        
        for c in util.CONFIG:
            widget = builder.get_object('{}_config'.format(c))
            if widget is not None:
                config_set_value(widget, util.get_config(c))
        
        dialog = ui['giqra'].get_object('settings_dialog')
        if dialog.run() == Gtk.ResponseType.OK:
            for c in util.CONFIG:
                widget = builder.get_object('{}_config'.format(c))
                if widget is not None:
                    value = config_get_value(widget)
                    t = type(util.CONFIG[c])
                    util.set_config(c, t(value))
        dialog.hide()
    
    @staticmethod
    def on_about_button_clicked(button):
        dialog = ui['giqra'].get_object('about_dialog')
        print(dialog.run())
        dialog.hide()
    
    @staticmethod
    def on_backup_button_clicked(button):
        try:
            util.backup()
        except Exception as e:
            dialog = Gtk.MessageDialog(
                ui['giqra'].get_object('main_win'),
                0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
                _('An error occurred!'))
            dialog.format_secondary_text(type(e).__name__)
            dialog.run()
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(ui['giqra'].get_object('main_win'),
            0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                _('Backup successfully completed.'))
            dialog.run()
            dialog.destroy()

def start_main():
    Gtk.main()
    for c in util.CONFIG:
        util.dump_config()


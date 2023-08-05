from iqra import db
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

N_ = lambda x: x
N_('stickers')

def connect_signals(builder, obj, signal_name, handler_name, connect_object,
        flags, plugin, util):
    obj.connect(signal_name, globals()[handler_name], builder, plugin, util)

def init_ui(builder):
    builder.get_object('stickers_items_liststore').clear()
    check_filters_show(builder)
    on_range_radiobutton_toggled(builder.get_object('range_radiobutton'),
        builder, None, None)
    on_pattern_radiobutton_toggled(builder.get_object('pattern_radiobutton'),
        builder, None, None)

def gui_config_update_tags_sample(widget, builder, plugin, util):
    builder.get_object('stickers_page_drawingarea').queue_draw()

def on_stickers_page_drawingarea_draw(area, ctx, builder, plugin, util):
    MM_IN_PT = 72 / 25.4
    
    config = {}
    for c in plugin.CONFIG:
        config[c] = config_get_value(builder.get_object(c))
    
    ow = config['stickers_page_width']
    oh = config['stickers_page_height']
    
    scaler = min(
        area.get_allocated_width() / MM_IN_PT / ow,
        area.get_allocated_height() / MM_IN_PT / oh
    )
    
    config['stickers_page_height'] *= scaler
    config['stickers_page_width'] *= scaler
    
    config['stickers_left_margin'] *= scaler
    config['stickers_top_margin'] *= scaler
    
    fontname, fontsize = config['stickers_font'].rsplit(maxsplit=1)
    config['stickers_font'] = '{} {}'.format(
        fontname, float(fontsize) * scaler)
    config['stickers_border_width'] *= scaler
    
    max_count = int(config['stickers_rows'] * config['stickers_columns'])
    remaining = max_count
    
    session = util.get_scoped_session()
    queries = []
    
    w = config['stickers_page_width'] * MM_IN_PT
    h = config['stickers_page_height'] * MM_IN_PT
    x = (area.get_allocated_width() - w) / 2
    y = (area.get_allocated_height() - h) / 2
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.translate(x, y)
    ctx.rectangle(0, 0, w, h)
    ctx.fill_preserve()
    ctx.clip()
    
    q = session.query(db.Library).limit(1)
    count = q.count()
    queries.append({'count': min(remaining, 1), 'q': q})
    remaining -= count
    
    q = session.query(db.Section).filter(db.Section.parent_id != None).limit(1)
    count = q.count()
    queries.append({'count': min(remaining, 1), 'q': q})
    remaining -= count
    
    q = session.query(db.Book).limit(1)
    count = q.count()
    queries.append({'count': min(remaining, max_count), 'q': q})
    remaining -= count
    
    plugin(util=util).call(ctx=ctx, queries=queries, config=config)

def filter_checkbutton_toggled(checkbutton, builder, plugin, util):
    check_filters_show(builder)

def on_item_combobox_changed(combobox, builder, plugin, util):
    check_filters_show(builder)

def check_filters_show(builder):
    check_filter_show(builder)
    check_range_show(builder)
    check_pattern_show(builder)

def check_filter_show(builder):
    active_id = builder.get_object('item_combobox').get_active_id()
    
    if active_id != 'none':
        builder.get_object('filter_checkbutton').show()
    else:
        builder.get_object('filter_checkbutton').hide()
    
    if not builder.get_object('filter_checkbutton').get_visible():
        builder.get_object('filter_checkbutton').set_active(False)

def check_range_show(builder):
    active_id = builder.get_object('item_combobox').get_active_id()
    
    cond = active_id in ['section', 'book']
    cond = cond and builder.get_object('filter_checkbutton').get_active()
    
    if cond:
        builder.get_object('range_radiobutton').show()
        builder.get_object('range_box').show()
    else:
        builder.get_object('range_radiobutton').hide()
        builder.get_object('range_box').hide()

def check_pattern_show(builder):
    active_id = builder.get_object('item_combobox').get_active_id()
    
    cond = active_id != 'none'
    cond = cond and builder.get_object('filter_checkbutton').get_active()
    
    if cond:
        builder.get_object('pattern_radiobutton').show()
        builder.get_object('pattern_entry').show()
    else:
        builder.get_object('pattern_radiobutton').hide()
        builder.get_object('pattern_entry').hide()
    
    if not builder.get_object('range_radiobutton').get_visible():
        builder.get_object('pattern_radiobutton').set_active(True)

def on_pattern_radiobutton_toggled(button, builder, plugin, util):
    value = button.get_active()
    builder.get_object('pattern_entry').set_sensitive(value)

def on_range_radiobutton_toggled(button, builder, plugin, util):
    value = button.get_active()
    builder.get_object('range_start_entry').set_sensitive(value)
    builder.get_object('range_end_entry').set_sensitive(value)

def on_add_item_button_clicked(button, builder, plugin, util):
    args = []
    args.append(builder.get_object('item_combobox').get_active_id())
    args.append('-c')
    args.append(str(builder.get_object('copies_spinbutton').get_value_as_int()))
    if builder.get_object('filter_checkbutton').get_active():
        if builder.get_object('range_radiobutton').get_active():
            args.append('-r')
            args.append(builder.get_object('range_start_entry').get_text())
            args.append(builder.get_object('range_end_entry').get_text())
        elif builder.get_object('pattern_radiobutton').get_active():
            args.append('-p')
            args.append(builder.get_object('pattern_entry').get_text())
    
    text = ' '.join(args)
    while len(args) < 6:
        args.append(None)
    
    args.append(text)
    
    builder.get_object('stickers_items_liststore').append(args)

def on_remove_item_button_clicked(button, builder, plugin, util):
    selection = builder.get_object('items_treeview').get_selection()
    model, idx = selection.get_selected()
    del model[idx]

def on_choose_file_button_clicked(button, builder, plugin, util):
    dialog = builder.get_object('save_dialog')
    dialog.set_current_name('Untitled.pdf')
    result = dialog.run()
    dialog.hide()
    if result == Gtk.ResponseType.OK:
        builder.get_object('file_entry').set_text(dialog.get_filename())

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
        return widget.get_active_id()
    elif isinstance(widget, Gtk.TextView):
        buf = widget.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
    else:
        print('could not get value from widget type `{}`'.format(type(widget)))

def start(builder, main_win):
    dialog = builder.get_object('start_dialog')
    dialog.set_transient_for(main_win)
    
    init_ui(builder)
    
    result = dialog.run()
    dialog.hide()
    
    if result == Gtk.ResponseType.OK:
        items = []
        for c in builder.get_object('stickers_items_liststore'):
            items.extend(c[:-1])
        
        return [], tuple(), {
            'items': [c for c in items if c is not None],
            'file': builder.get_object('file_entry').get_text(),
        }


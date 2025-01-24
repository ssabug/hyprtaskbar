import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import astal
 
class AppButton(astal.Widget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        button = Gtk.Button()
        icon = Gtk.Image.new_from_gicon(app.get_icon(), Gtk.IconSize.LARGE_TOOLBAR)
        button.set_image(icon)
        button.connect('clicked', self.on_clicked)
        self.set_child(button)
 
    def on_clicked(self, button):
        self.app.launch()
 
class AppLauncher(astal.Widget):
    def __init__(self):
        super().__init__()
        box = Gtk.FlowBox()
        box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_child(box)
 
        apps = Gio.AppInfo.get_all()
        for app in apps:
            if app.should_show():
                box.add(AppButton(app))
 
class MyWindow(astal.Window):
    def __init__(self):
        super().__init__(title="App Launcher")
        self.set_child(AppLauncher())
 
astal.init()
window = MyWindow()
window.present()
astal.run()
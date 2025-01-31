import math
import os
import json
import subprocess
from gi.repository import (
    AstalIO,
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalBattery as Battery,
    AstalWp as Wp,
    AstalNetwork as Network,
    AstalTray as Tray,
    AstalMpris as Mpris,
    AstalHyprland as Hyprland,
    AstalApps as Apps
)
from utils import *


SYNC = GObject.BindingFlags.SYNC_CREATE
#CONFIG_FILE="config.json"
       
class Workspaces(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Workspaces"])
        hypr = Hyprland.get_default()
        hypr.connect("notify::workspaces", self.sync)
        hypr.connect("notify::focused-workspace", self.sync)
        self.sync()
        self.log("workspaces loaded");

    def log(self,msg,severity="INFO"):
        log(msg,source="MEDI",severity=severity)

    def sync(self, *_):
        hypr = Hyprland.get_default()
        for child in self.get_children():
            child.destroy()

        for ws in hypr.get_workspaces():
            if not (ws.get_id() >= -99 and ws.get_id() <= -2): # filter out special workspaces
                self.add(self.button(ws))

    def button(self, ws):
        hypr = Hyprland.get_default()
        btn = Gtk.Button(visible=True)
        btn.add(Gtk.Label(visible=True, label=ws.get_id()))

        if hypr.get_focused_workspace() == ws:
            Astal.widget_set_class_names(btn, ["focused"])

        btn.connect("clicked", lambda *_: ws.focus())
        return btn

class StartButton(Gtk.Box):
    def __init__(self) -> None:
        super().__init__();
        btn = Gtk.Button(visible=True)

        img=getConfigParam("startButton.image");
        if img != "" and img != None and os.path.exists(img) and getConfigParam("startButton.enableImage"):
            image = Gtk.Image();
            image.set_from_file(img);     
            btn.add(image);

        text=getConfigParam("startButton.text");
        if text != "" and text != None:
            btn.add(Gtk.Label(visible=True, label="START"));
        
        self.startMenuCommand=getConfigParam("startButton.command")
        self.add(btn);
        btn.connect("clicked", self.clicked)
        self.log("start button loaded");

    def log(self,msg,severity="INFO"):
        log(msg,source="STBU",severity=severity)

    def clicked(self,whocares) -> None:
        processname = "rofi"
        tmp = os.popen("ps -Af").read()
        proccount = tmp.count(processname)
        if proccount > 0:
            os.system("killall " + processname)
        else:
            os.system(self.startMenuCommand);

class QuickLaunch(Gtk.Box):
    def __init__(self) -> None:
        super().__init__();

        Astal.widget_set_class_names(self, ["Launcher"])
        Astal.widget_set_css(self, "min-width: 140px")
        box=Gtk.Box()
        scrollWindow=Gtk.ScrolledWindow();
        #self.queryProgramList("");
        progamList=getConfigParam("quickLaunch.programList");

        for program in progamList:
            app=self.queryProgramList(program);
            if len(app)> 0:
                app=app[0];
                btn = Gtk.Button(visible=True);
                image = Gtk.Image();
                #pixbuf = Gdk.pixbuf_new_from_file(self.getIconPath(app['icon']))
                #pixbuf = pixbuf.scale_simple(30, 30, gtk.gdk.INTERP_BILINEAR)
                #image.set_from_pixbuf(pixbuf);
                image.set_from_icon_name(app["icon"],3)
                #image.set_from_file(self.getIconPath(app['icon']);
                btn.connect("clicked",self.runProgram,app["executable"])
                #btn.add(Gtk.Label(visible=True, label=app['name']));
                btn.add(image);
                box.add(btn);
        

        self.add(box);
        self.log("app launcher client loaded");

    def log(self,msg,severity="INFO"):
        log(msg,source="QKLC",severity=severity);

    def queryProgramList(self,text):
        results=[];

        self.apps = Apps.Apps(
            name_multiplier=2,
            entry_multiplier=0,
            executable_multiplier=2,
        )

        for app in self.apps.fuzzy_query(text):
            results.append({
                            "name":app.get_name(),
                            "icon":app.get_icon_name(),
                            "executable":app.get_executable()    
                            });

        return results

    def getIconPath(self,text):
        cmd='find /usr/share/icons | grep ' + text
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate();
        path=str(out.strip().decode('UTF-8'))
        if '\n' in path:
            path=path.split("\n")[0]

        return path

    def runProgram(self,dontcare,executable):
        executable+=" &"
        executable=executable.replace(" %u","")
        executable=executable.replace(" %U","")
        os.system(executable);
        print(executable)
        #t=executable.split(" ")
        #subprocess.call(t)

class FocusedClient(Gtk.Label):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Focused"])
        Hyprland.get_default().connect("notify::focused-client", self.sync)
        self.sync();
        self.log("focused client loaded");

    def log(self,msg,severity="INFO"):
        log(msg,source="FOCC",severity=severity)

    def sync(self, *_):
        client = Hyprland.get_default().get_focused_client()
        if client is None:
            return self.set_label("")

        client.bind_property("title", self, "label", SYNC)

class Media(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        self.players = {}
        mpris = Mpris.get_default()
        Astal.widget_set_class_names(self, ["Media"])
        mpris.connect("notify::players", self.sync)
        self.sync();
        self.log("media loaded");

    def log(self,msg,severity="INFO"):
        log(msg,source="MEDI",severity=severity)

    def sync(self):
        mpris = Mpris.get_default()
        for child in self.get_children():
            child.destroy()

        if len(mpris.get_players()) == 0:
            self.add(Gtk.Label(visible=True, label="Nothing Playing"))
            return

        player = mpris.get_players()[0]
        label = Gtk.Label(visible=True)
        cover = Gtk.Box(valign=Gtk.Align.CENTER)
        Astal.widget_set_class_names(cover, ["Cover"])

        self.add(cover)
        self.add(label)

        player.bind_property(
            "title",
            label,
            "label",
            SYNC,
            lambda *_: f"{player.get_artist()} - {player.get_title()}",
        )

        def on_cover_art(*_):
            Astal.widget_set_css(
                cover, f"background-image: url('{player.get_cover_art()}')"
            )

        id = player.connect("notify::cover-art", on_cover_art)
        cover.connect("destroy", lambda _: player.disconnect(id))
        on_cover_art()

class SysTray(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["SysTray"])
        self.items = {}
        tray = Tray.get_default()
        tray.connect("item_added", self.add_item)
        tray.connect("item_removed", self.remove_item)
    
        self.log("system tray loaded");

    def log(self,msg,severity="INFO"):
        log(msg,source="TRAY",severity=severity)

    def add_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            return

        item = Tray.get_default().get_item(id)
        btn = Gtk.MenuButton(use_popover=False, visible=True)
        icon = Astal.Icon(visible=True)

        item.bind_property("tooltip-markup", btn, "tooltip-markup", SYNC)
        item.bind_property("gicon", icon, "gicon", SYNC)
        item.bind_property("menu-model", btn, "menu-model", SYNC)
        btn.insert_action_group("dbusmenu", item.get_action_group())

        def on_action_group(*args):
            btn.insert_action_group("dbusmenu", item.get_action_group())

        item.connect("notify::action-group", on_action_group)

        btn.add(icon)
        self.add(btn)
        self.items[id] = btn

    def remove_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            del self.items[id]

class NetworkInfo(Astal.Icon):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Wifi"])
        wifi = Network.get_default().get_wifi()
        if wifi:
            wifi.bind_property("ssid", self, "tooltip-text", SYNC)
            wifi.bind_property("icon-name", self, "icon", SYNC)

        self.log("network loaded")
    def log(self,msg,severity="INFO"):
        log(msg,source="NTWK",severity=severity)

class Audio(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Audio"])
        Astal.widget_set_css(self, "min-width: 140px")
        box=Gtk.Box()
        
        
        #icon.add_events()
        #icon.connect("clicked", self.mute)
        slider = Astal.Slider(hexpand=True);
        volumeAmount=Gtk.Button();
        volumeAmount.add(Gtk.Label(visible=True, label="0%"))

        icon = Astal.Icon();
        button=Gtk.Button(visible=True) ;
        button.add(icon);
        button.connect("clicked", self.get_settings) 

        box.add(button);
       

        eventBox=self.createVolumeScroll();
        volumeAmount.connect('scroll-event', self.on_scroll);

        box.add(eventBox)
        

        self.add(box);
        self.add(slider)#slider

        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("volume-icon", icon, "icon", SYNC)
        speaker.bind_property("volume", slider, "value", SYNC)
        slider.connect("dragged", lambda *_: speaker.set_volume(slider.get_value()))
        
        self.speaker=speaker;

        self.log("audio loaded")

    def log(self,msg,severity="INFO"):
        log(msg,source="AUDI",severity=severity)

    def on_scroll(self, widget):
        # Handles zoom in / zoom out on Ctrl+mouse wheel
        '''
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            direction = event.get_scroll_deltas()[2]
            print(direction);
        else:
            print("scroll error");
        '''
        self.log(str(widget))

    def createVolumeScroll(self):
        eventBox= Gtk.EventBox()
        eventBox.add_events(21)
        #eventBox.connect("scroll-event",self.changeVolume )
        eventBox.connect('scroll-event', self.on_scroll)
        #eventBox.connect("dragged", lambda *_: speaker.set_volume(slider.get_value()))
        return eventBox;

    def get_settings(self,unused):
        os.system(getConfigParam("audio.settingsCommand"))

    def changeVolume(self,unused):
        speaker.set_volume(self.box.slider.get_value());

    def mute(self,unused):

        speaker=self.speaker;

        if speaker.get_value() == 0:
            speaker.set_volume(100);
        else:
            speaker.set_volume(0);

class BatteryLevel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Battery"])

        icon = Astal.Icon()
        label = Astal.Label()

        self.add(icon)
        self.add(label)

        bat = Battery.get_default()
        bat.bind_property("is-present", self, "visible", SYNC)
        bat.bind_property("battery-icon-name", icon, "icon", SYNC)
        bat.bind_property(
            "percentage",
            label,
            "label",
            SYNC,
            lambda _, value: f"{math.floor(value * 100)}%",
        )

        self.log("battery level loaded")

    def log(self,msg,severity="INFO"):
        log(msg,source="BTLV",severity=severity)

class Time(Astal.Label):
    def __init__(self, format=""):
        super().__init__();
        if format == "":
            self.format = getConfigParam("time.displayFormat")
        else:
            self.format = format
        self.interval = AstalIO.Time.interval(1000, self.sync)
        self.connect("destroy", self.interval.cancel);

        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self.clicked)
        #self.connect("button-press-event",self.clicked)
        Astal.widget_set_class_names(self, ["Time"]);

        self.log("time loaded")

    def sync(self):
        self.set_label(GLib.DateTime.new_now_local().format(self.format))

    def clicked(self,balek,rab):
        self.log("CLIQUEZ BANDE DE PUTES");
        self.log(str(balek))

    def log(self,msg,severity="INFO"):
        log(msg,source="TIME",severity=severity)

class Left(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(hexpand=True, halign=Gtk.Align.START)
        position = "left"
        for widget in getConfig().keys():
            classname=widget[0].upper()+widget[1:]
            if getConfigParam(widget+".position") == position:
               self.add(eval(classname+"()")) 

class Center(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        position = "center"
        for widget in getConfig().keys():
            classname=widget[0].upper()+widget[1:]
            if getConfigParam(widget+".position") == position:
               self.add(eval(classname+"()")) 
               
class Right(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(hexpand=True, halign=Gtk.Align.END)
        position = "right"
        for widget in getConfig().keys():
            classname=widget[0].upper()+widget[1:]
            if getConfigParam(widget+".position") == position:
               self.add(eval(classname+"()")) 

class Bar(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor):
        super().__init__(
            anchor=Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.RIGHT
            | Astal.WindowAnchor.TOP,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
        )

        Astal.widget_set_class_names(self, ["Bar"])

        self.add(
            Astal.CenterBox(
                start_widget=Left(),
                center_widget=Center(),
                end_widget=Right(),
            )
        )

        self.show_all()

#!/usr/bin/env python3
import sys
import versions
import subprocess
import os
from gi.repository import AstalIO, Astal, Gio
from widget.Bar import *
from pathlib import Path
from utils import *

homeFolder=getGlobalParam("appHomeFolder");

if "${HOME}" in homeFolder:
    homeFolder=homeFolder.replace("${HOME}",os.path.expanduser("~"));

if os.path.exists(homeFolder):
    scss = os.path.join(homeFolder,"style.scss");
    css = "/tmp/style.css";
else:
    print("ERROR app folder not found : " + homeFolder);
    exit()

class App(Astal.Application):
    def do_astal_application_request(
        self, msg: str, conn: Gio.SocketConnection
    ) -> None:
        self.log(msg)
        AstalIO.write_sock(conn, "hello")

    def do_activate(self) -> None:
        self.hold()
        subprocess.run(["sass", scss, css])
        self.apply_css(css, True)
        for mon in self.get_monitors():
            self.add_window(Bar(mon));
            self.log("hyprtaskbar loaded, scss : " + scss + ", css : " + css)

    def log(self,msg,severity="INFO"):
        log(msg,source="GTKG",severity=severity)

instance_name = "python"
app = App(instance_name=instance_name)

if __name__ == "__main__":
    log("hyprtaskbar launched",source="GTKG");
    try:
        app.acquire_socket()
        app.run(None)
        log("hyprtaskbar stopped",source="GTKG");
    except Exception as e:
        msg=AstalIO.send_message(instance_name, "".join(sys.argv[1:]));
        handleErrors(e);
        log("hyprtaskbar stopped with exception",source="GTKG",severity="ERROR");

    log('////////////////////////////////////////////////////////////////////////////////////////',source="GTKG");

# hyprtaskbar
A simple Astal taskbar for hyprland inspired by [simple-bar](https://github.com/Aylur/astal/tree/main/examples/gtk3/py/simple-bar)

## Install
 - you need the following linux binaries : git,zip,unzip,pip
 - you need the following python libs : pycairo,PyGObject,PyInstaller,levenshtein
 - build with `git clone https://github.com/ssabug/hyprtaskbar && cd hyprtaskbar ` 
 - run `./utils/install_linux.sh` it will copy binary into **/usr/share/hyprtaskbar** and user data in **~/.config/hyprtaskbar/**

## Running
 - run `hyprtaskbar` for one time use, or
 - add the following line to your `~/.config/hypr/hyprland.conf` file : `exec = cd /usr/share/hyprtaskbar && ./hyprtaskbar` for persistence

## License
WTFPL
all trashtalk rights reserved if bad behaviour with the program
